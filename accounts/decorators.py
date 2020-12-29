from django.shortcuts import redirect
from django.http import HttpResponse


#view_func is the decorated function ,الفنشكن الي هنزود فيها ال functionality
def authenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper(requset,*args,**kwargs):
            group=None

            if requset.user.groups.exists():
                group=requset.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(requset,*args,**kwargs)
            elif group == 'customer':
                return redirect('user')
            elif group =='admin':
                return redirect('home')
        return wrapper
    return decorator

