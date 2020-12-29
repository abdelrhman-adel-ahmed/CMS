from django import forms
from django.forms import ModelForm
from .models import Order,Customer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class OrderFormForAdmin(ModelForm):
    
    class Meta():
        model=Order
        fields='__all__'
       # exclude=['customer','date_created']



class OrderFormForUsers(ModelForm):
    class Meta():
        model=Order
        fields='__all__'
        exclude=['customer','date_created','status']

class CreationUserForm(UserCreationForm):
    email=forms.EmailField(required=True)

    class Meta:
        model=User
        fields=['username','email','password1','password2']

class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields='__all__'
        exclude=['user']