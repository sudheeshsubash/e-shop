from django.db import models
from django.contrib.auth.models import AbstractUser



custom_user_role_choice = (
        ('admin','Admin'),
        ('shopadmin','Shop Admin'),
        ('shopstaff','Shop Staff'),
        ('enduser','User'),
    )

class CustomUser(AbstractUser):
    '''
    custom user (change auth user inbuild table)
    '''
    phone_number = models.BigIntegerField(null=True,unique=True)
    role = models.CharField(max_length=10,choices=custom_user_role_choice)

    class Meta:
        verbose_name = 'CustomUser'




class ShopCategorys(models.Model):
    '''
    shop category (main categorys of shops)
    '''
    shop_category_name = models.CharField(max_length=50,null=False,unique=True)
    discribe = models.TextField()




class ShopDetails(CustomUser):
    '''
    shop details
    '''
    place = models.CharField(max_length=30)
    address = models.CharField(max_length=100)
    varify = models.BooleanField(default=False)
    ownername = models.CharField(max_length=30)
    shop_category = models.ForeignKey("superadmin.ShopCategorys", on_delete=models.CASCADE,related_name='shopcategory')

    class Meta:
        verbose_name = 'ShopDetails'




class ProductsCategorys(models.Model):
    '''
    shop products
    '''
    product_category_name = models.CharField(max_length=50,null=False,unique=True)
    shop_category = models.ForeignKey("superadmin.ShopCategorys", on_delete=models.CASCADE,related_name='categoryofproductcategory')
    shop = models.ForeignKey("superadmin.ShopDetails", on_delete=models.CASCADE,related_name='shop',null=True)




class ShopStaff(CustomUser):
    '''
    shop staff
    '''
    shop = models.ForeignKey("superadmin.ShopDetails", on_delete=models.CASCADE,null=False,related_name='shopstaff')

    class Meta:
        verbose_name = 'ShopStaff'




class ShopProducts(models.Model):
    '''
    products
    '''
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    stock = models.IntegerField()
    date_of_create = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    discription = models.TextField()
    shop = models.ForeignKey("superadmin.ShopDetails", on_delete=models.CASCADE,related_name='eshops')
    categoryid = models.ForeignKey("superadmin.ProductsCategorys", on_delete=models.CASCADE,related_name='productcategory')
    variation = models.ForeignKey("superadmin.ProductVariation", on_delete=models.CASCADE,related_name='variation')


class ProductImages(models.Model):
    '''
    dynamic images apply in products
    '''
    product = models.ForeignKey("superadmin.ShopProducts", on_delete=models.CASCADE,related_name='products')
    image = models.ImageField(upload_to='images/', max_length=200)



class ProductVariation(models.Model):
    variation_name = models.CharField(max_length=50,null=False,unique=True)




class EndUserCart(models.Model):
    '''
    cart
    '''
    user = models.ForeignKey("superadmin.CustomUser", on_delete=models.CASCADE,related_name='user')
    product = models.ForeignKey("superadmin.ShopProducts", on_delete=models.CASCADE,related_name='product')
    quantity = models.IntegerField(default=1)
    total_amount = models.IntegerField(null=False)





class EndUserWishlist(models.Model):
    '''
    wishlist
    '''
    user = models.ForeignKey("superadmin.CustomUser", on_delete=models.CASCADE,related_name='users')
    product = models.ForeignKey("superadmin.ShopProducts", on_delete=models.CASCADE,related_name='productss')



status_choice = (
    ('pending','Pending'),
    ('cancel','Cancel'),
    ('complete','Complete'),
    ('refund','Refund'),
)

payment_choice = (
    ('cashonhand','Cash On hand'),
    ('online','Online'),
)


class EndUserOrders(models.Model):
    '''
    EndUser Orders
    '''
    shop = models.ForeignKey("superadmin.ShopDetails", on_delete=models.CASCADE,related_name='ordershop')
    user = models.ForeignKey("superadmin.CustomUser", on_delete=models.CASCADE,related_name='orederuser')
    staff = models.ForeignKey("superadmin.ShopStaff", on_delete=models.CASCADE,null=True,related_name='orderstaff')
    payment_credit = models.IntegerField(null=True)
    payment_debit = models.IntegerField(null=True)
    payment_id = models.CharField(max_length=25,null=True)
    order_id = models.CharField(max_length=25,null=True)
    total_amount = models.IntegerField()
    order_status = models.CharField(max_length=20,choices=status_choice)
    payment_type = models.CharField(max_length=20,choices=payment_choice)
    create = models.DateTimeField(auto_now_add=True)



class OrderProducts(models.Model):
    '''
    Orders Product list
    '''
    order = models.ForeignKey("superadmin.EndUserOrders", on_delete=models.CASCADE,related_name='productorder')
    shop = models.ForeignKey("superadmin.ShopDetails", on_delete=models.CASCADE)
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=30)
    product_price = models.IntegerField()
    quantity = models.IntegerField()
    total = models.IntegerField()
    discription = models.TextField()
