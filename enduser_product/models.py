from django.db import models


class EndUserCart(models.Model):
    '''
    cart
    '''
    user = models.ForeignKey("admin_app1.CustomUser", on_delete=models.CASCADE)
    product = models.ForeignKey("eshopadmin_product.ShopProducts", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(null=False)



class EndUserWishlist(models.Model):
    '''
    wishlist
    '''
    user = models.ForeignKey("admin_app1.CustomUser", on_delete=models.CASCADE)
    product = models.ForeignKey("eshopadmin_product.ShopProducts", on_delete=models.CASCADE)