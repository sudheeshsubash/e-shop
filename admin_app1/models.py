from django.db import models
from django.contrib.auth.models import AbstractUser

choice = (
        ('admin','Admin'),
        ('shopadmin','Shop Admin'),
        ('shopstaff','Shop Staff'),
        ('enduser','User'),
    )

class CustomUser(AbstractUser):
    
    phone_number = models.BigIntegerField(null=True,unique=True)
    role = models.CharField(max_length=10,choices=choice)