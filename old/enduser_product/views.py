from rest_framework.decorators import api_view,permission_classes
from .serializers import EndUserCartSerializer,EndUserViewProductsSerializer,EndUserWishlistSerializer
from admin_app1.tokens_permissions import CustomEndUserPermission,get_decoded_payload
from rest_framework import filters
from django_filters import rest_framework as filters
from admin_app1.paginations import CustomPageNumberPagination
from eshopadmin_product.models import ShopProducts
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import EndUserCart


class UserProductFilter(filters.FilterSet):
    '''
    eshop detail filtering class
    '''
    class Meta:
        model = ShopProducts
        fields = ['name']




class ShowAllProductsChoosedShop(APIView):
    '''
    show products from selected shopid
    '''
    permission_classes=[CustomEndUserPermission]

    def get(self, request):
        shopid = request.query_params.get('sid')
        if shopid is None:
            return Response({'error':'pass sid(shop id) to query params'})
        print(shopid)
        try:
            products = ShopProducts.objects.filter(shop_id_id=shopid)
        except ShopProducts.DoesNotExist:
            return Response({'msg':f'{shopid} is not valid'})
        pagination = CustomPageNumberPagination()
        user_filter = UserProductFilter(request.query_params, queryset=products)
        result = pagination.paginate_queryset(user_filter.qs,request)
        serializer = EndUserViewProductsSerializer(result, many=True)
        return pagination.get_paginated_response(serializer.data)



class CartManagementForEndUser(APIView):
    '''
    cart management add, incresequantity, decresequantity, remove
    '''
    permission_classes=[CustomEndUserPermission]


    def post(self, request):
        pid = request.query_params.get('pid')
        if pid is None:
            return Response({'error':'pass pid(product id) to query params'})
        user_id_decode = get_decoded_payload(request=request)
        cart_serializer = EndUserCartSerializer(request.data)
        cart = cart_serializer.save(user_id=user_id_decode['user_id'],product_id=pid)
        return Response({'msg':f'{cart.product.name} added to cart'})



    def get(self, request):
        user_id_decode = get_decoded_payload(request=request)
        try:
            cartdetails = EndUserCart.objects.filter(user = user_id_decode['user_id'])
        except EndUserCart.DoesNotExist:
            return Response({'msg':'no cart data'})
        return Response({'cart products':f"{cartdetails}"})



    def delete(self, request):
        cart_id = request.query_params.get('cid')
        if cart_id is None:
            return Response({'error':'pass cid(cart id) to query params'})
        cart = EndUserCartSerializer(request.data)
        cartname = cart.product.name
        cart.remove(cart_id=cart_id)
        return Response({'product':f'productname : {cartname} removed','id':f'cartid : {cart_id} removed'})



    def patch(self, request):
        type = request.query_params.get('type')
        cid = request.query_params.get('cid')
        if  type is None or cid is None:
            return Response({'error':'query params is needed "type" and "cid"'})
        if str(type) == 'increse':
            cart = EndUserCartSerializer(request.data)
            quantity = cart.increse_quantity(cart_id=cid)
            if quantity:
                if quantity == 'error':
                    return Response({'cart' :f'id :{cid} is not valid'})
                return Response({'msg':f'quantity is {quantity}'})
            return Response({'msg':'limited stock'})
        
        elif str(type) == 'decrese':
            cart = EndUserCartSerializer(request.data)
            quantity = cart.decrese_quantity(cart_id=cid)
            if quantity:
                if quantity == 'error':
                    return Response({'cart':f'id :{cid} is not valid'})
                return Response({'msg':f'quantity is {quantity}'})
            return Response({'msg':f'quantit is {quantity} cart data deleted'})





class WishlistManagementForEnduser(APIView):
    '''
    wishlist management add , remove , wishlist to cart
    '''


    def get(self, request):
        pass



    def post(self, request):
        pass



    def delete(self, request):
        pass

 