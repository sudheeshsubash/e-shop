from rest_framework.views import APIView
from rest_framework.response import Response
from superadmin.tokengeneratedecode import get_decoded_payload,get_tokens_for_user,check_jwt_user_id_kwargs_id
from superadmin.custompermissions import CustomShopAdminPermission
from .serializers import ShopCategoryOrMagerCategorySerializer,RegistrationShopDetailsSerializer,EditProductCategorySerializer
from .serializers import RegistrationShopDetailsOtpConfirmationSerializer,ProductCategorySerializer,AddProductCategorySerializer
from superadmin.models import ShopCategorys,ShopDetails,ProductsCategorys
from superadmin.otps import otp
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from superadmin.serializers import LoginSerializer
from django.contrib.auth import authenticate,login,logout
from rest_framework import status






class ShopRegistration(APIView):
    '''
    shop registration
    '''
    def get(self, request):
        result = dict()
        try:
            shopcategory_from_database = ShopCategorys.objects.all().values('shop_category_name','id')
        except ShopCategorys.DoesNotExist:
            pass
        shopcategory_serializer = ShopCategoryOrMagerCategorySerializer(shopcategory_from_database,many=True)
        result['shop_category'] = Response(shopcategory_serializer.data).data
        result['username']=''
        result['phone_number']=''
        result['address']=''
        result['place']=''
        result['ownername']=''
        result['email']=''
        result['password']=''
        return Response(result)


    def post(self, request):
        registration_form_data_serializer = RegistrationShopDetailsSerializer(data=request.data)
        if registration_form_data_serializer.is_valid(raise_exception=True):
            otpnumber = otp(phone=registration_form_data_serializer.data.get('phone_number')) # here otp number sent to phone number

            request.session['username'] = registration_form_data_serializer.data.get('username')
            request.session['password'] = registration_form_data_serializer.data.get('password')
            request.session['phone_number'] = registration_form_data_serializer.data.get('phone_number')
            request.session['place'] = registration_form_data_serializer.data.get('place')
            request.session['address'] = registration_form_data_serializer.data.get('address')
            request.session['ownername'] = registration_form_data_serializer.data.get('ownername')
            request.session['email'] = registration_form_data_serializer.data.get('email')
            request.session['shop_category'] = registration_form_data_serializer.data.get('shop_category')
            request.session['otpnumber'] = otpnumber()

            return Response({"otp":f'otp sended to phone'})
            


class RegistrationOtpConfirm(APIView):
    '''
    
    '''
    def get(self, request):
        return Response({'result':"required value, pass OTP number to query param (otpnumber),"})


    def post(self, request):
        otpnumber = request.query_params.get('otpnumber')
        if otpnumber is None:
            return Response({'result':'Enter or Pass otpnumber to query params'})
        print(otpnumber)
        print(type(otpnumber))
        print(request.session.get('otpnumber'))
        print(type(request.session.get('otpnumber')))
        if int(otpnumber) != request.session.get('otpnumber',None):
            return Response({'result':'otpnumber is not valid'})
        
        shopcategory = ShopCategorys.objects.get(id=request.session.get('shop_category'))
        
        shop = ShopDetails.objects.create(
                username = request.session.get('username',None),
                password = make_password(request.session.get('password',None)),
                email = request.session.get('email',None),
                place = request.session.get('place',None),
                address = request.session.get('address',None),
                ownername = request.session.get('ownername',None),
                phone_number = request.session.get('phone',None),
                shop_category = shopcategory,
                role = 'shopadmin',
        )
        request.session.flush()
        shop_serializer = RegistrationShopDetailsOtpConfirmationSerializer(shop,many=True)
        shop_details = Response(shop_serializer.data).data
        return Response({"result":f"{shop_details} is created"})




class ShopAdminDashBord(APIView):
    '''
    shop admin dashbord
    '''
    permission_classes=[CustomShopAdminPermission]
    
    def get(self, request, *args, **kwargs):
        if check_jwt_user_id_kwargs_id(request,kwargs['shopid']):
            return Response('shop admin dashbord')
        return Response({'result':'You dont have permission for access this api'})



class ShopAdminLogin(APIView):
    '''
    
    '''
    def get(self, request, *args, **kwargs):
        login_serializer_data = LoginSerializer(request.data)
        if login_serializer_data.validate():
            username = login_serializer_data.data.get('username')
            password = login_serializer_data.data.get('password')
            users = authenticate(username=username,password=password)
            if users is not None:
                if users.id == kwargs['shopid']:
                    token = get_tokens_for_user(user=users)
                    login(request,users)
                    return Response({'token':token},status=status.HTTP_200_OK)
            return Response({'error':f'{username} and {password} is not correct'},status=status.HTTP_401_UNAUTHORIZED)
        return Response('login')



class ViewAllProductCategoryGlobelAndCustomCategorys(APIView):
    '''
    this is show all globel and custom categorys
    '''
    permission_classes=[CustomShopAdminPermission]

    def get(self, request, *args, **kwargs):
        if not check_jwt_user_id_kwargs_id(request,kwargs['shopid']):
            return Response({'error':"You have no permission for access this shop method"})
        try:
            product_category_query = ProductsCategorys.objects.filter(Q(shop__isnull=True)|Q(shop=kwargs['shopid']))
        except ProductsCategorys.DoesNotExist:
            return Response({'error':'No Product categorys'})
        
        product_category_serializer = ProductCategorySerializer(product_category_query,many=True)
        return Response(product_category_serializer.data)


    # def get(self, request):
    #     takeshopid_from_token = get_decoded_payload(request)
    #     try:
    #         product_category_query = ProductsCategorys.objects.filter(Q(shop__isnull=True)|Q(shop=takeshopid_from_token['user_id']))
    #     except ProductsCategorys.DoesNotExist:
    #         return Response({'error':'No Product categorys'})
        
    #     product_category_serializer = ProductCategorySerializer(product_category_query,many=True)
    #     return Response(product_category_serializer.data)



class CustomizeProductCategoryOrEditAddCategory(APIView):
    '''
    this is possible for (Add,Edit)(GET,POST,PATCH) methods
    '''
    permission_classes = [CustomShopAdminPermission]

    def get(self, request):
        customize_type = request.query_params.get('type')
        if customize_type is None:
            return Response({'pass query param value like ?type=add (or) edit'})
        
        if customize_type == 'add':
            return Response({'result':'required form field, Enter the value "product_category_name"'})
        
        if customize_type != 'edit':
            return Response({'not valid type'})
        
        custom_product_category_id = request.query_params.get('categoryid')
        takeshopid_from_token = get_decoded_payload(request)
        if custom_product_category_id is None:
            return  Response({'pass (categoryid) in query param'})
        try:
            product_category_query = ProductsCategorys.objects.filter(id=custom_product_category_id,shop=takeshopid_from_token['user_id']).values('product_category_name')
        except ProductsCategorys.DoesNotExist:
            return Response({'error':'No exist Product categorys'})
        
        product_category_serializer = EditProductCategorySerializer(product_category_query,many=True)
        return Response(product_category_serializer.data)
        


    def post(self, request):
        customize_type = request.query_params.get('type')
        if customize_type is None:
            return Response({'pass query param value like ?type=add'})
        
        if customize_type != 'add':
            return Response({'only ?type=add is valid of post method'})
        
        takeshopid_from_token = get_decoded_payload(request)
        try:
            shop_details = ShopDetails.objects.get(id=takeshopid_from_token['user_id'])
        except ShopDetails.DoesNotExist:
            return Response({'error':'shop is not valid'})
        
        product_category_serializer = AddProductCategorySerializer(data=request.data)
        if product_category_serializer.is_valid(raise_exception=True):
            custom_product_category = ProductsCategorys.objects.create(
                product_category_name = product_category_serializer.data.get('product_category_name'),
                shop=shop_details,shop_category=shop_details.shop_category
            )
            custom_product_category_serializer = ProductCategorySerializer(custom_product_category)
            return Response(custom_product_category_serializer.data)



    def patch(self, request):
        customize_type = request.query_params.get('type')
        product_category_id = request.query_params.get('productid')
        takeshopid_from_token = get_decoded_payload(request)

        if customize_type is None or product_category_id is None:
            return Response({'result':'pass (type) and (productid) to query params'})
        if customize_type != 'edit':
            return Response({'result':'only ?type=edit is valid'})
        
        try:
            customize_product_category_query = ProductsCategorys.objects.get(id=product_category_id,shop=takeshopid_from_token['user_id'])
        except ProductsCategorys.DoesNotExist:
            return Response({'error':f'{product_category_id} is not valid'})
        
        product_category_serializer = EditProductCategorySerializer(customize_product_category_query,data=request.data)
        if product_category_serializer.is_valid(raise_exception=True):
            product_category_serializer.save()
            return Response(product_category_serializer.data)
        return Response({"error":'Enter a valid credetials'})