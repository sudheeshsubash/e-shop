from rest_framework.views import APIView
from superadmin.paginations import CustomPageNumberPagination
from superadmin.models import ShopProducts,ProductImages,CustomUser,EndUserCart,EndUserWishlist
from shopadmin_product_management.serializers import ShopProductSerializer,ProductImageSerializer
from django_filters import rest_framework as filters
from rest_framework.response import Response
from superadmin.otps import otp
from .serializers import RegistrationUserSerializer,RegistrationQuerysetToSerializer,UserCartSerializer,UserWishlistSerializer
from .serializers import UserAddProductToWishlistSerializer
from django.contrib.auth.hashers import make_password
from superadmin.tokengeneratedecode import get_decoded_payload
from superadmin.custompermissions import CustomEndUserPermission


class UserRegistration(APIView):
    '''
    user registration
    '''
    def get(self, request):
        result = dict()
        result['username']=''
        result['phone_number']=''
        result['password']=''
        result['confirm_password']=''
        return Response(result)


    def post(self, request):
        registration_form_data_serializer = RegistrationUserSerializer(data=request.data)
        if registration_form_data_serializer.is_valid(raise_exception=True):
            otpnumber = otp(phone=registration_form_data_serializer.data.get('phone_number')) # here otp number sent to phone number
            print(otpnumber())
            request.session['username'] = registration_form_data_serializer.data.get('username')
            request.session['password'] = registration_form_data_serializer.data.get('password')
            request.session['phone_number'] = registration_form_data_serializer.data.get('phone_number')
            request.session['otpnumber'] = otpnumber()

            return Response({"otp":f'otp sended to your phone'})
            


class RegistrationOtpConfirm(APIView):
    '''
    
    '''
    def get(self, request):
        return Response({'result':"required value, pass OTP number to query param (otpnumber),"})


    def post(self, request):
        otpnumber = request.query_params.get('otpnumber')
        if otpnumber is None:
            return Response({'result':'Enter or Pass otpnumber to query params'})
        if int(otpnumber) != request.session.get('otpnumber',None):
            return Response({'result':'otpnumber is not valid'})
        
        user = CustomUser.objects.create(
                username = request.session.get('username',None),
                password = make_password(request.session.get('password',None)),
                phone_number = request.session.get('phone_number',None),
                role = 'enduser',
        )
        request.session.flush()
        shop_serializer = RegistrationQuerysetToSerializer(user,many=False)
        shop_details = Response(shop_serializer.data).data
        return Response({"result":f"{shop_details} is created"})






class UserProductFilter(filters.FilterSet):
    '''
    eshop detail filtering class
    '''
    class Meta:
        model = ShopProducts
        fields = ['name','price']


class ViewAllProductsForUser(APIView):
    '''
    view all the products, Add pagination and filters
    '''
    def get(self, request):
        
        pagination = CustomPageNumberPagination()
        try:
            all_products_query = ShopProducts.objects.all()
        except ShopProducts.DoesNotExist:
            return Response('No products found in the shop')
        filter_products = UserProductFilter(request.query_params,queryset=all_products_query)
        pages = pagination.paginate_queryset(filter_products.qs,request)
        product_serializer = ShopProductSerializer(pages,many=True)

        for product in product_serializer.data:
            product_image_query = ProductImages.objects.filter(product=product['id'])
            product_image_serializer = ProductImageSerializer(product_image_query,many=True)

            product['image'] = product_image_serializer.data
        return pagination.get_paginated_response(product_serializer.data)
    


class AddToCartGuestUserAndAuthenticatedUser(APIView):
    '''
    
    '''
    permission_classes = [CustomEndUserPermission]


    def get(self, request):
        user_id_from_jwt_token = get_decoded_payload(request)

        cart_queryset = EndUserCart.objects.filter(user = user_id_from_jwt_token['user_id'])
        result = dict()
        result_list = list()
        for item in range(len(cart_queryset)):
            shop_product_queryset = ShopProducts.objects.get(id=cart_queryset[item].product.id)
            shop_product_serializer = ShopProductSerializer(shop_product_queryset,many=False)
            result_list.append({'product':shop_product_serializer.data})
            result_list.append({'cartquantity':cart_queryset[item].quantity})
            result_list.append({'total amount':cart_queryset[item].total_amount})
            result[f"cartid {cart_queryset[item].id}"] = result_list
        return Response(result)


    def post(self, request):
        product_id_from_query_params = request.query_params.get('productid')
        if product_id_from_query_params is None:
            return Response({'result':'(?productid=value) is need pass to query param'})
        if not ShopProducts.objects.filter(id=product_id_from_query_params).exists():
            return Response({'result':'productid is not valid'})
        if request.user.is_authenticated:
            user_id_decode = get_decoded_payload(request=request)
            cart_serializer = UserCartSerializer(request.data,many=False)
            cart = cart_serializer.save(user_id=user_id_decode['user_id'],product_id=product_id_from_query_params)
            result_response = UserCartSerializer(cart,many=False)
            return Response(result_response.data)
    


    def patch(self, request):
        type = request.query_params.get('type')
        cartid = request.query_params.get('cartid')
        if  type is None or cartid is None:
            return Response({'error':'query params is needed "type" and "cartid"'})
        if str(type) == 'increse':
            cart = UserCartSerializer(request.data)
            quantity = cart.increse_quantity(cart_id=cartid)
            if quantity:
                if quantity == 'error':
                    return Response({'cart' :f'id :{cartid} is not valid'})
                return Response({'msg':f'quantity is {quantity}'})
            return Response({'msg':'limited stock'})
        
        elif str(type) == 'decrese':
            cart = UserCartSerializer(request.data)
            quantity = cart.decrese_quantity(cart_id=cartid)
            if quantity:
                if quantity == 'error':
                    return Response({'cart':f'id :{cartid} is not valid'})
                return Response({'msg':f'quantity is {quantity}'})
            return Response({'msg':f'quantit is {quantity} cart data deleted'})
    

    def delete(self, request):
        cart_id = request.query_params.get('cartid')
        if cart_id is None:
            return Response({'error':'cartid is needed as a query param'})
        try: 
            EndUserCart.objects.get(id=cart_id).delete()
        except EndUserCart.DoesNotExist:  # added this line to catch exception when the object does not exist 
            return Response({'error': 'No object found with the given id'})
        return Response({'result':f'{cart_id} is removed from cart'})



class AddToGueWishliststUserAndAuthenticatedUser(APIView):
    '''
    
    '''
    permission_classes = [CustomEndUserPermission]

    def get(self, request, *args, **kwargs):
        user_id_from_jwttoken = get_decoded_payload(request=request)
        wishlist_query = EndUserWishlist.objects.filter(user=user_id_from_jwttoken['user_id'])
        result = dict()
        for item in range(len(wishlist_query)):
            shop_product_queryset = ShopProducts.objects.get(id=wishlist_query[item].product.id)
            shop_product_serializer = ShopProductSerializer(shop_product_queryset,many=False)
            shop_product_serializer.data['wishlist']=wishlist_query[item]
            result[f"wishlistid {wishlist_query[item].id}"] = shop_product_serializer.data
        if result:
            return Response(result)
        return Response({"result":'No wishlist product'})


    def post(self, request, *args, **kwargs):
        user_id_from_jwttoken = get_decoded_payload(request=request)
        product_id_from_query_params = request.query_params.get('productid')
        if product_id_from_query_params is None:
            return Response({'result':'(?productid=value) is need pass to query param'})
        if not ShopProducts.objects.filter(id=product_id_from_query_params).exists():
            return Response({'result':'productid is not valid'})
        try:
            EndUserWishlist.objects.get(product=product_id_from_query_params)
        except EndUserWishlist.DoesNotExist:
            return_wishlist_query = EndUserWishlist.objects.create(
                user_id = user_id_from_jwttoken['user_id'],
                product_id = product_id_from_query_params
            )
            result_serializer = UserWishlistSerializer(return_wishlist_query)
            return Response(result_serializer.data)
        return Response({'result':'product is already saved'})


    def delete(self, request):
        wishlist_id_from_query_param = request.query_params.get('wishlistid')
        if wishlist_id_from_query_param is None:
            return Response({'result':'(?wishlistid=value) is needed'})
        try:
            EndUserWishlist.objects.get(id=wishlist_id_from_query_param).delete()
        except EndUserWishlist.DoesNotExist:
            return Response({'error':'wishlist id is not valid'})
        return Response({'result':'product remove from wishlist'})


    def put(self, request, *args, **kwargs):
        return Response('this is put method')
