from eshopadmin_product.models import ShopProducts
from rest_framework import serializers
import re
from .models import EndUserCart,EndUserWishlist




class EndUserViewProductsSerializer(serializers.ModelSerializer):
    '''
    shop products serializer
    '''
    class Meta:
        model = ShopProducts
        fields = '__all__'




class EndUserCartSerializer(serializers.ModelSerializer):
    '''
    end user product add to cart database serializer
    '''
    class Meta:
        model=EndUserCart
        fields=''

    def save(self, user_id, product_id):
        '''
        custom save method parameters user id and produt id 
        the fetch price data and save to endusercart database
        '''
        products = ShopProducts.objects.values_list('price').get(id=product_id)
        return EndUserCart.objects.create(
            user_id = user_id,
            product_id = product_id,
            price = products.price
        )

    @staticmethod
    def increse_quantity(cart_id):
        '''
        increse cart quantity, check product stock and cart quantity
        '''
        cart = EndUserCart.objects.get(id=cart_id)
        produt = ShopProducts.objects.get(id=cart.product.id)
        if cart.quantity+1 >= produt.stock:
            return 0
        
        cart.quantity += 1
        cart.save()
        return cart.quantity

    @staticmethod
    def decrese_quantity(cart_id):
        '''
        decrese cart quantity, check cart quantity is 0 
        then delete the cart queryset
        '''
        cart = EndUserCart.objects.get(id=cart_id)
        if cart.quantity-1 == 0:
            cart.delete()
            return 0
        cart.quantity -= 1
        cart.save()
        return cart.quantity


    @staticmethod
    def remove(cart_id):
        EndUserCart.objects.get(id=cart_id).delete()




class EndUserWishlistSerializer(serializers.ModelSerializer):
    '''
    wishlist
    '''
    class Meta:
        model=EndUserWishlist
        fields=''


    def save(self, user_id, product_id):
        '''
        
        '''
        return EndUserWishlist.objects.create(
            user_id=user_id,
            product_id = product_id
        )
    

    @staticmethod
    def remove(wishlist_id):
        EndUserWishlist.objects.get(id=wishlist_id).delete()


    @staticmethod
    def wishlist_to_cart(wishlist_id):
        wishlist = EndUserWishlist.objects.get(id=wishlist_id)
        return EndUserCart.objects.create(
            user_id = wishlist.user.id,
            product_id = wishlist.product.id,
            price = wishlist.product.price
        )