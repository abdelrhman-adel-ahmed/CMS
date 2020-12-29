from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponseRedirect
from django.views import View
from .models import*
from .forms import OrderFormForAdmin,OrderFormForUsers,CreationUserForm,CustomerForm
from django.forms import inlineformset_factory
from .filters import OrderFilter,CustomerFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .decorators import authenticated_user,allowed_users
from django.contrib.auth.models import Group

class Home(View):

    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['admin']))
    def get(self, request):
        orders=Order.objects.all()
        customers=Customer.objects.all()

        total_num_customers=customers.count()
        total_num_orders=orders.count()
        deliverd=orders.filter(status="Deliverd").count()
        pending=orders.filter(status="Pending").count()
        out_for_delivery=orders.filter(status="Out for delivery").count()

        context={
            'orders':orders,
            'customers':customers,
            'total_num_customers':total_num_customers,
            'total_num_orders':total_num_orders,
            'deliverd':deliverd,
            'pending':pending,
            'out_for_delivery':out_for_delivery
        }
        return render(request,'accounts/dashboard.html',context) 


class product(View):
    def get(self, request):
        products=Product.objects.all()
        context = {
            'products':products
            }
        return render(request,'accounts/products.html',context) 


class customer(View):

    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['admin']))
    def get(self, request,id):
        customer=Customer.objects.get(id=id)
        orders=customer.order_set.all()
        #orderfilter take orders and the request.get date which is our search ,the it filter the orders based on the 
        #request.get parameters ,then we can acess these filted query set by the qs property function
        filter=OrderFilter(request.GET,queryset=orders)
        orders=filter.qs

        context={
            'customer':customer,
            'orders':orders,
            'filter':filter
        }
        return render(request,'accounts/customer.html',context) 

class CreateCustomer(View):

    def get(self,request):
        form=CreationUserForm()
        context={
            'form':form,
        }
        return render(request,'accounts/create_customer.html',context)

    def post(self,request):
        form=CreationUserForm(request.POST)
        context={
            'form':form,
        }
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request,'accounts/create_customer.html',context)


class customer_list(View):

    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['admin']))
    def get(self, request):
        customers=Customer.objects.all()
        filter=CustomerFilter(request.GET,queryset=customers)
        customers=filter.qs
        context={
            'customers':customers,
            'filter':filter
        }
        return render(request,'accounts/customer_list.html',context) 


class CreateOrder(View):
    
    @method_decorator(login_required(login_url='login'))
    def get(self,request,id):
        customer=Customer.objects.get(id=id)
        # OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'))
        # form=OrderFormSet()
        form=OrderFormForAdmin(initial={'customer':customer})
        context={
            'form':form,
            }
        return render(request,'accounts/order_form.html',context)

    def post(self,request,id):
        form=OrderFormForAdmin(request.POST)
        #OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'))
        #form=OrderFormSet(request.POST,instance=customer)
        customer=Customer.objects.get(id=id)
        context={
            'form':form
        }
        if form.is_valid():
            form.save()
            return redirect('customer',id=id)
        else:
            return render(request,'accounts/order_form.html',context)

class UpdateOrder(View):
    template_name='accounts/update_form.html'
    
    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['admin']))
    def get(self,request,id):
        order=Order.objects.get(id=id)
        form=OrderFormForAdmin(request.POST or None,instance=order)
        context={
            'form':form
        }
        return render(request,self.template_name,context)

    def post(self,request,id):
        order=Order.objects.get(id=id)
        form=OrderFormForAdmin(request.POST or None,instance=order)
        context={
            'form':form
        }
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            return render(request,self.template_name,context)

class DeleteOrder(View):
    
    @method_decorator(login_required(login_url='login'))
    def get(self,requset,id):
        order=Order.objects.get(id=id)
        form=OrderFormForAdmin(instance=order)
        context={
            'order':order,
            'form':form
        }
        return render(requset,'accounts/delete.html',context)

    def post(self,requset,id):
        order=Order.objects.get(id=id)
        order.delete()            
        return redirect('home')

class Register(View):

    @method_decorator(authenticated_user)
    def get(self,request):
        form=CreationUserForm()
        context={
            'form':form,
        }
        return render(request,'accounts/register.html',context)

    def post(self,request):
        form=CreationUserForm(request.POST)
        context={
            'form':form,
        }
        if form.is_valid():
            user=form.save()
            #will usee signal instead
            # group=Group.objects.get(name="customer")
            # #add the user attribute to the row
            # Customer.objects.create(    
            #     user=user,
            #     name=user.username,
            #     email=user.email,
            #     )
            # user.groups.add(group)
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
        else: return render(request,'accounts/register.html',context)

class Login(View):

    @method_decorator(authenticated_user)
    def get(self,request):
        # if request.user.is_authenticated:
        #     return redirect('home')
        # else:
        return render(request,'accounts/login.html')
        
    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        #returns a User object if the password is valid for the given username. If the password is invalid returns None
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else: 
            messages.info(request, f'Wrong username or password')
            return redirect('login')

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('login')

    def post(self,request):
        pass


class User(View):
    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['customer']))
    def get(self,request):
        user_id=request.user.id
        #get the id of the user and then go to customer table filed of the f.k that point to users and get that row
        customer=Customer.objects.get(user_id=user_id)
        
        orders=customer.order_set.all()
        total_num_orders=orders.count()
        #orders=request.user.customer.order_set.all()
        # deliverd=customer.order_set.filter(status="Delivered").count()
        # pending=customer.order_set.filter(status="Pending").count()
        # out_for_delivery=customer.order_set.filter(status='Out for delivery').count()
        deliverd=orders.filter(status="Delivered").count()
        pending=orders.filter(status="Pending").count()
        out_for_delivery=orders.filter(status='Out for delivery').count()
        context={
            'orders':orders,
            'total_num_orders':total_num_orders,
            'deliverd':deliverd,    
            'pending':pending,
            'out_for_delivery':out_for_delivery
        }
        return render(request,'accounts/user.html',context)

class User_Setting(View):

    @method_decorator(login_required(login_url='login'))
    @method_decorator(allowed_users(allowed_roles=['customer']))
    def get(self,request):

        form=CustomerForm(instance=request.user.customer)
        context={
            'form':form,
        }
        return render(request,'accounts/profile_setting.html',context)

    def post(self,request):
        #without instance= // form will not change why ??!!
        form=CustomerForm(request.POST,request.FILES,instance=request.user.customer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('User_Setting')

