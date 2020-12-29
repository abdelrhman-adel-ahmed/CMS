from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Customer
from django.contrib.auth.models import Group

#after User get create it issue signal to this and post_save (after save method take palce) it create customer

def create_customer_profile(sender,instance,created,**kwargs):
    if created:
        group=Group.objects.get(name="customer")
        instance.groups.add(group)
        Customer.objects.create(    
                user=instance,
                name=instance.username,
                email=instance.email,
                )

post_save.connect(create_customer_profile,sender=User)


