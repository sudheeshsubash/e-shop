from django.db import models



class ShopCategorys(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    



class ShopProducts(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    stock = models.IntegerField()
    date_of = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True)
    image1 = models.ImageField(upload_to='images/', max_length=200)
    image2 = models.ImageField(upload_to='images/', max_length=200)
    shop_id = models.ForeignKey("eshopadmin_app1.ShopDetails", on_delete=models.CASCADE)
    category_id = models.ForeignKey("eshopadmin_product.ShopCategorys", on_delete=models.CASCADE)




class ProductImages(models.Model):
    product = models.ForeignKey("eshopadmin_product.ShopProducts", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', max_length=200)