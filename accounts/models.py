from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=200,null=True)
    phone=models.CharField(max_length=200,null=True)
    email=models.EmailField(null=True)
    data_created=models.DateTimeField(auto_now_add=True)
    prof_pic=models.ImageField(default='default.png',null=True)
    
    #when you print the object, and what you see in the adimin pannel when you open the table to see the rows 
    #by defult it print the object p.k(id)  
    def __str__(self):
        return self.name

class Tag(models.Model):
    name=models.CharField(max_length=200,null=True)
    
    def __str__(self):
        return self.name 


class Product(models.Model):
    CATEGORY=(
        ('Indoor','Indoor'),
        ('Out Door','Out Door')
    )
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField(null=True)
    category=models.CharField(max_length=200,null=True,choices=CATEGORY)
    description=models.CharField(max_length=200,null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    tags=models.ManyToManyField(Tag)

    def __str__(self):
        return self.name 


class Order(models.Model):
    STATUS=(
        ('Pending','Pending'),
        ('Out for delivery','Out for delivery'),
        ('Deliverd','Deliverd')
    )
    #on_delte if the paretnt got deleted (customer) what we want to do with child(Order) here we delete the child 
    #one to many relation (one customer can have many orders)
    #one product can have many orders order that product (e.x علبه صلصله معفنه كذا اورور ممكن يكون فيه علبه الصلصله)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date_created=models.DateTimeField(auto_now_add=True)    
    status=models.CharField(max_length=190,null=True,choices=STATUS)
    note=models.CharField(max_length=190,null=True,blank=True)
    

    def __str__(self):
        return self.product.name