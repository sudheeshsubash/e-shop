from rest_framework.decorators import api_view,permission_classes
from .serializers import EndUserCartSerializer,EndUserViewProductsSerializer,EndUserWishlistSerializer
from admin_app1.tokens_permissions import CustomEndUserPermission,get_decoded_payload
from rest_framework import filters
from django_filters import rest_framework as filters
from admin_app1.paginations import CustomPageNumberPagination
from eshopadmin_product.models import ShopProducts
from rest_framework.response import Response




class UserProductFilter(filters.FilterSet):
    '''
    eshop detail filtering class
    '''
    class Meta:
        model = ShopProducts
        fields = ['name']
    

@api_view(['GET'])
@permission_classes([CustomEndUserPermission])
def view_all_products(request,shopid):
    '''
    view all products of selected shop
    and filtering by name and place 
    also add paginations to.
    '''
    products = ShopProducts.objects.filter(shop_id_id=shopid)
    pagination = CustomPageNumberPagination()
    user_filter = UserProductFilter(request.query_params, queryset=products)
    result = pagination.paginate_queryset(user_filter.qs,request)
    serializer = EndUserViewProductsSerializer(result, many=True)
    return pagination.get_paginated_response(serializer.data)



@api_view(['POST'])
@permission_classes([CustomEndUserPermission])
def add_to_cart(request,pid):
    '''
    product add to cart
    '''
    if request.method == 'POST':
        user_id_decode = get_decoded_payload(request=request)
        cart_serializer = EndUserCartSerializer(request.data)
        cart = cart_serializer.save(user_id=user_id_decode['user_id'],product_id=pid)
        return Response({'msg':f'{cart} added to cart'})



@api_view(['GET'])
@permission_classes([CustomEndUserPermission])
def insrese_cart_quantity(request,cid):
    '''
    cart database increst cart quentity
    '''
    cart = EndUserCartSerializer(request.data)
    quantity = cart.increse_quantity(cart_id=cid)
    if quantity:
        return Response({'msg':f'quantity is {quantity}'})
    return Response({'msg':'limited stock'})




@api_view(['GET'])
@permission_classes([CustomEndUserPermission])
def decrese_cart_quantity(request,cid):
    '''
    cart database decrese cart product quantity
    '''
    cart = EndUserCartSerializer(request.data)
    quantity = cart.decrese_quantity(cart_id=cid)
    if quantity:
        return Response({'msg':f'quantity is {quantity}'})
    return Response({'msg':f'quantit is {quantity} cart data deleted'})



@api_view(['GET'])
@permission_classes([CustomEndUserPermission])
def remove_to_cart(request,cid):
    cart = EndUserCartSerializer(request.data)
    cart.remove(cart_id=cid)
    return Response({'msg':'removed'})




@api_view(['GET'])
@permission_classes([CustomEndUserPermission])
def add_to_wishlist(request,pid):
    user_id_decode = get_decoded_payload(request=request)
    wishlist_serializer = EndUserWishlistSerializer(request.data)
    wishlist = wishlist_serializer.save(user_id=user_id_decode['user_id'],product_id=pid)
    return Response({'msg':f'{wishlist} added to cart'})



@api_view(['GET'])
@permission_classes([CustomEndUserPermission])
def remove_to_wishlist(request,wid):
    wishlist = EndUserWishlistSerializer(request.data)
    wishlist.remove(wid)
    return Response({'msg':'removed'})





@api_view(['GET'])
@permission_classes([CustomEndUserPermission])
def add_wishlist_to_cart(request,wid):
    wishlistToCart = EndUserWishlistSerializer(request.data)
    returnvalue = wishlistToCart.wishlist_to_cart(wishlist_id=wid)
    return Response({"msg":f"wishlist data to cart, successfully added {returnvalue}"})