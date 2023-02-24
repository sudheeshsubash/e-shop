from django.db import models
from django.contrib.auth.models import User
from admin_app1.models import CustomUser

class ShopDetails(CustomUser):
    place = models.CharField(max_length=30)
    address = models.CharField(max_length=100,null=True)
    varify = models.BooleanField(default=True)
    ownername = models.CharField(max_length=30)



class ShopStaff(CustomUser):
    shop_id = models.ForeignKey("eshopadmin_app1.ShopDetails", on_delete=models.CASCADE,null=False)