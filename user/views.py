from rest_framework.views import APIView
from superadmin.paginations import CustomPageNumberPagination
from superadmin.models import ShopProducts,ProductImages,CustomUser,EndUserCart,EndUserWishlist,UsersDetails,ShopDetails
from shopadmin_product_management.serializers import ShopProductSerializer,ProductImageSerializer
from django_filters import rest_framework as filters
from rest_framework.response import Response
from superadmin.otps import otp
from .serializers import RegistrationUserSerializer,RegistrationQuerysetToSerializer,UserCartSerializer,UserWishlistSerializer
from .serializers import UserAddProductToWishlistSerializer,ViewProductSerializer,OtpEnter,LoginSerializer
from django.contrib.auth.hashers import make_password
from superadmin.tokengeneratedecode import get_decoded_payload,get_tokens_for_user,check_valid_shop_userid
from superadmin.custompermissions import CustomEndUserPermission
from django.contrib.auth import authenticate,login
from rest_framework import status




class UserRegistration(APIView):
    '''
    user registration
    '''
    def get(self, request, *args, **kwargs):
        result = dict()
        result['username']=''
        result['phone_number']=''
        result['password']=''
        result['confirm_password']=''
        return Response(result)

    def post(self, request, *args, **kwargs):
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
    def get(self, request, *args, **kwargs):
        return Response({'result':"required value, pass OTP number to query param (otpnumber),"})

    def post(self, request, *args, **kwargs):
        try:
            shop_kwargs_check = ShopDetails.objects.get(id=kwargs['shopid'])
        except ShopDetails.DoesNotExist:
            return Response({"error":"this api is not valid"})
        otp_serializer = OtpEnter(request.data)
        if int(otp_serializer.data.get('otp')) != request.session.get('otpnumber',None):
            return Response({'result':'otpnumber is not valid'})
        
        user = UsersDetails.objects.create(
                username = request.session.get('username',None),
                password = make_password(request.session.get('password',None)),
                phone_number = request.session.get('phone_number',None),
                role = 'enduser',
                shop_id = shop_kwargs_check.id,
        )
        request.session.flush()
        shop_serializer = RegistrationQuerysetToSerializer(user,many=False)
        shop_details = Response(shop_serializer.data).data
        return Response({"result":f"{shop_details} is created"})




class LoginUser(APIView):

    def get(self, request, *args, **kwargs):
        login_serializer = LoginSerializer(request.data) 
        if login_serializer.validate():
            username = login_serializer.data.get('username')
            password = login_serializer.data.get('password')
            users = authenticate(username=username,password=password)
            if users is not None:
                try:
                    user_details = UsersDetails.objects.get(customuser_ptr_id=users.id)
                except Exception as e:
                    return Response(e)
                if int(user_details.shop.id) == kwargs['shopid']:
                    token = get_tokens_for_user(user=users)
                    login(request,users)
                    return Response({'token':token},status=status.HTTP_200_OK)
            return Response({'error':f'{username} and {password} is not correct'},status=status.HTTP_401_UNAUTHORIZED)


    

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

    def get(self, request, *args, **kwargs):
        
        pagination = CustomPageNumberPagination()
        try:
            all_products_query = ShopProducts.objects.filter(shop=kwargs['shopid'])
        except ShopProducts.DoesNotExist:
            return Response('No products found in the shop')
        filter_products = UserProductFilter(request.query_params,queryset=all_products_query)
        pages = pagination.paginate_queryset(filter_products.qs,request)
        product_serializer = ShopProductSerializer(pages,many=True)

        for product in product_serializer.data:
            product_image_query = ProductImages.objects.filter(product=product['id'])
            product_image_serializer = ProductImageSerializer(product_image_query[0],many=False)
            product['image'] = product_image_serializer.data
        return pagination.get_paginated_response(product_serializer.data)



class ViewProductsDetails(APIView):
    '''
    
    '''

    def get(self, request, *args, **kwargs):
        user_id_from_jwttoken = get_decoded_payload(request)

        product_details_query = ShopProducts.objects.filter(id=user_id_from_jwttoken['user_id'])
        if not product_details_query:
            return Response({"error":"product is not exist"})
        product_details_serializer = ViewProductSerializer(product_details_query,many=True)

        product_image_query = ProductImages.objects.filter(product=product_details_serializer.data[0]['id'])
        if not product_image_query:
            product_details_serializer['image'] = "DoesNotExist image"
        else:
            product_image_serializer = ProductImageSerializer(product_image_query,many=True)
            product_details_serializer.data[0]['image'] = product_image_serializer.data
        
        return Response({"result":product_details_serializer.data})




class AllCartViewGuestUserAuthenticatedUser(APIView):
    '''
    view all cart products
    '''
    permission_classes = [CustomEndUserPermission]

    def get(self, request, *args, **kwargs):
        if check_valid_shop_userid(request,kwargs['shopid']):
            return Response({"error":"You don't have permission for access this shop api"})
        
        cart_queryset = EndUserCart.objects.filter(shop=kwargs['shopid'])
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



class UserAddProductToCart(APIView):
    '''
    
    '''
    permission_classes = [CustomEndUserPermission]

    def post(self, request, *args, **kwargs):
        if check_valid_shop_userid(request,kwargs['shopid']):
            return Response({"error":"You don't have permission for access this shop api"})
        
        payload = get_decoded_payload(request)
        cart_serializer = UserCartSerializer(request.data)
        user_cart_data = cart_serializer.save(
            user_id=payload['user_id'],
            product_id=kwargs['productid'],
            shop_id=kwargs['shopid']
        )
        user_cart_serializer = UserCartSerializer(user_cart_data,many=False)
        return Response(user_cart_serializer.data)



class QuantityDelete(APIView):
    '''
    
    '''
    permission_classes = [CustomEndUserPermission]

    def patch(self, request, *args, **kwargs):
        if check_valid_shop_userid(request,kwargs['shopid']):
            return Response({"error":"You don't have permission for access this shop api"})
        
        type = request.query_params.get('type')
        # cartid = request.query_params.get('cartid')
        if  type is None:
            return Response({'error':'query params is needed "type"'})
        if str(type) == 'increse':
            cart = UserCartSerializer(request.data)
            quantity = cart.increse_quantity(cart_id=kwargs['cartid'])
            if quantity:
                if quantity == 'error':
                    return Response({'cart' :f'id :{kwargs["cartid"]} is not valid'})
                return Response({'msg':f'quantity is {quantity}'})
            return Response({'msg':'limited stock'})
        
        elif str(type) == 'decrese':
            cart = UserCartSerializer(request.data)
            quantity = cart.decrese_quantity(cart_id=kwargs['cartid'])
            if quantity:
                if quantity == 'error':
                    return Response({'cart':f'id :{kwargs["cartid"]} is not valid'})
                return Response({'msg':f'quantity is {quantity}'})
            return Response({'msg':f'quantit is {quantity} cart data deleted'})
    

    def delete(self, request, *args, **kwargs):
        if check_valid_shop_userid(request,kwargs['shopid']):
            return Response({"error":"You don't have permission for access this shop api"})
        try: 
            EndUserCart.objects.get(id=kwargs['cartid']).delete()
        except EndUserCart.DoesNotExist:  # added this line to catch exception when the object does not exist 
            return Response({'error': 'No object found with the given id'})
        return Response({'result':f'{kwargs["cartid"]} is removed from cart'})



class AllWishlistView(APIView):

    permission_classes = [CustomEndUserPermission]
    
    def get(self, request, *args, **kwargs):
        if check_valid_shop_userid(request,kwargs['shopid']):
            return Response({"error":"You don't have permission for access this shop api"})
        user_id_from_jwttoken = get_decoded_payload(request)

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



class AddToWishlist(APIView):

    permission_classes = [CustomEndUserPermission]

    def post(self, request, *args, **kwargs):
        if check_valid_shop_userid(request,kwargs['shopid']):
            return Response({"error":"You don't have permission for access this shop api"})
        user_id_from_jwttoken = get_decoded_payload(request)

        try:
            EndUserWishlist.objects.get(product=kwargs['productid'])
        except EndUserWishlist.DoesNotExist:
            return_wishlist_query = EndUserWishlist.objects.create(
                user_id = user_id_from_jwttoken['user_id'],
                product_id = kwargs['productid']
            )
            result_serializer = UserWishlistSerializer(return_wishlist_query)
            return Response(result_serializer.data)
        return Response({'result':'product is already saved'})
    

 

class EditWishlist(APIView):

    permission_classes = [CustomEndUserPermission]

    def delete(self, request, *args, **kwargs):
        if check_valid_shop_userid(request,kwargs['shopid']):
            return Response({"error":"You don't have permission for access this shop api"})
        try:
            EndUserWishlist.objects.get(id=kwargs['wishlistid']).delete()
        except EndUserWishlist.DoesNotExist:
            return Response({'error':'wishlist id is not valid'})
        return Response({'result':'product remove from wishlist'})



class WishlistToCart(APIView):
    '''
    
    '''
    permission_classes = [CustomEndUserPermission]

    def put(self, request, *args, **kwargs):
        if check_valid_shop_userid(request,kwargs['shopid']):
            return Response({"error":"You don't have permission for access this shop api"})
        payload = get_decoded_payload(request)
        wishlist_query = EndUserWishlist.objects.filter(user=payload['user_id'])
        if not wishlist_query:
            return Response({"error":"Wishlist is Empty"})
        result = list()
        for wishlist in wishlist_query:
            try:
                cart = EndUserCart.objects.get(user=payload['user_id'],product=wishlist.product)
            except EndUserCart.DoesNotExist:
                cart = EndUserCart.objects.create(
                    shop_id = kwargs['shopid'],
                    product_id = wishlist.product.id,
                    user_id = payload['user_id'],
                    total_amount = wishlist.product.price
                )
            amount = cart.total_amount/cart.quantity
            cart.quantity += 1
            cart.total_amount = cart.quantity*amount
            cart.save()
            wishlist.delete()
            result.append(cart)

        cart_serializer = UserCartSerializer(result,many=True)
        return Response({"result":cart_serializer.data})

