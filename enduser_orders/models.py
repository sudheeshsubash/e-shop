from django.db import models


status_choice = (
    ('pending','Pending'),
    ('cancle','Cancle'),
    ('complete','Complete'),
)

payment_choice = (
    ('cashonpurchase','Cash On Purchase'),
    ('onlinepurchase','Online Purchase'),
)

class EndUserOrders(models.Model):
    '''
    EndUser Orders
    '''
    shop = models.ForeignKey("eshopadmin_app1.ShopDetails", on_delete=models.CASCADE,related_name='shop')
    user = models.ForeignKey("admin_app1.CustomUser", on_delete=models.CASCADE,related_name='user')
    staff = models.ForeignKey("eshopadmin_app1.ShopStaff", on_delete=models.CASCADE,related_name='staff',null=True)
    payment_id = models.CharField(max_length=25,null=True)
    order_id = models.CharField(max_length=25,null=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=20,choices=status_choice)
    payment_type = models.CharField(max_length=20,choices=payment_choice)
    create = models.DateTimeField(auto_now_add=True)



class OrderProducts(models.Model):
    '''
    Orders Product list
    '''
    order = models.ForeignKey("enduser_orders.EndUserOrders", on_delete=models.CASCADE,related_name='order')
    product = models.ForeignKey("eshopadmin_product.ProductImages", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=30)
    product_price = models.IntegerField()
    quantity = models.IntegerField()
    total = models.IntegerField()
