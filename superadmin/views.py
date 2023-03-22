from rest_framework.views import APIView
from .serializers import LoginSerializer,MainCategoryShopCategorySerializer,ShopRegistrationOtpSerializer
from django.contrib.auth import authenticate,login,logout
from .tokengeneratedecode import get_tokens_for_user,check_jwt_user_id_kwargs_id
from rest_framework.response import Response
from rest_framework import status
from .models import ShopDetails,ShopCategorys,ProductsCategorys
from .custompermissions import CustomAdminPermission
from rest_framework.decorators import permission_classes
from shopadmin.serializers import ShopCategoryOrMagerCategorySerializer,RegistrationShopDetailsSerializer
from shopadmin.serializers import RegistrationShopDetailsOtpConfirmationSerializer,ProductCategorySerializer
from .serializers import AddGlobelShopCategorySerializers,ProductCategorySerializers
from superadmin.otps import otp
from django.contrib.auth.hashers import make_password




class LoginSuperAdminEndUserShopAdminShopStaff(APIView):
    '''
    this is login for all roles superadmin,
    eshopadmin, eshopstaff, enduser
    '''
    def post(self, request):
        if request.user.is_authenticated:
            return Response({'status':'already login'})
        login_serializer_data = LoginSerializer(request.data)
        if login_serializer_data.validate():
            username = login_serializer_data.data.get('username')
            password = login_serializer_data.data.get('password')
            users = authenticate(username=username,password=password)
            if users is not None:
                if users.is_superuser:
                    token = get_tokens_for_user(user=users)
                    login(request,users)
                    return Response({'token':token},status=status.HTTP_200_OK)
            return Response({'error':f'{username} and {password} is not correct'},status=status.HTTP_401_UNAUTHORIZED)
        

    @permission_classes([CustomAdminPermission])
    def delete(self, request):
        '''
        loogout
        '''
        if request.user.is_authenticated:
            logout(request=request)
            return Response({'logout successfuly'})
        return Response({'login':'pass the access token'})
        


class SuperAdminDashBord(APIView):
    '''
    superadmin dashbord graph
    '''
    permission_classes=[CustomAdminPermission]

    def get(self, request):
        return Response('superadmin dashbord')



class ShopBlcokUnblock(APIView):
    '''
    superadmin can block shop account 
    '''
    permission_classes=[CustomAdminPermission]

    def patch(self, request, *args, **kwargs):

        try:
            shop_query = ShopDetails.objects.get(id=kwargs['shopid'])
        except ShopDetails.DoesNotExist:
            return Response({'error':f'{kwargs["shopid"]} is not valid'},status=status.HTTP_400_BAD_REQUEST)
        
        if shop_query.is_active:
            shop_query.is_active=False
            shop_query.save()
            return Response({'response':f'{shop_query.username} is blocked'},status=status.HTTP_200_OK)
        shop_query.is_active=True
        shop_query.save()
        return Response({'response':f'{shop_query.username} is  Unblocked'},status=status.HTTP_200_OK)



class ShopCategoryView(APIView):

    permission_classes = [CustomAdminPermission]

    def get(self, request, *args, **kwargs):
        try:
            shopcategory_from_database = ShopCategorys.objects.all()
        except ShopCategorys.DoesNotExist:
            return Response({'error':'no main categorys'})
        
        shopcategory_serializer = MainCategoryShopCategorySerializer(shopcategory_from_database,many=True)
        return Response(shopcategory_serializer.data)
    


class AddShopCategory(APIView):

    permission_classes = [CustomAdminPermission]

    def get(self, request, *args, **kwargs):
        return Response({"shop_category_name":'Enter the category name','discribe':'Discribe that category'})


    def post(self, request, *args, **kwargs):
        category_serializer = MainCategoryShopCategorySerializer(data=request.data)
        if category_serializer.is_valid(raise_exception=True):
            category_serializer.save()
            category = Response(category_serializer.data).data
            return Response(category)



class EditShopCategory(APIView):

    permission_classes = [CustomAdminPermission]

    def get(self, request, *args, **kwargs):
        try:
            category_from_database = ShopCategorys.objects.get(id=kwargs['categoryid'])
        except ShopCategorys.DoesNotExist:
            return Response({'error':f'{kwargs["categoryid"]} is not valid or (categoryi)d is not valid'})
        
        category_serializer = MainCategoryShopCategorySerializer(category_from_database)
        return Response(category_serializer.data)
    

    def patch(self, request, *args, **kwargs):
        try:
            category_from_database = ShopCategorys.objects.get(id=kwargs['categoryid'])
        except ShopCategorys.DoesNotExist:
            return Response({'categoryid':f'{kwargs["categoryid"]} is not valid'})
        
        category_serializer = MainCategoryShopCategorySerializer(category_from_database,data=request.data)
        if category_serializer.is_valid(raise_exception=True):
            category_serializer.save()
            return Response(category_serializer.data)
        
    
    def delete(self, request, *args, **kwargs):
        try:
            ShopCategorys.objects.get(id=kwargs['categoryid']).delete()
        except ShopCategorys.DoesNotExist:
            return Response({"error":"Category is not exist"})
        return Response({"result":"ShopCategory is deleted"})



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
            print(otpnumber())
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
        otp_serializer = ShopRegistrationOtpSerializer(request.data)
        if int(otp_serializer.data.get('otp')) != request.session.get('otpnumber',None):
            return Response({'result':'otpnumber is not valid'})
        
        shopcategory = ShopCategorys.objects.get(id=request.session.get('shop_category'))
        
        shop = ShopDetails.objects.create(
                username = request.session.get('username',None),
                password = make_password(request.session.get('password',None)),
                email = request.session.get('email',None),
                place = request.session.get('place',None),
                address = request.session.get('address',None),
                ownername = request.session.get('ownername',None),
                phone_number = request.session.get('phone_number',None),
                shop_category = shopcategory,
                role = 'shopadmin',
        )
        request.session.flush()
        shop_serializer = RegistrationShopDetailsOtpConfirmationSerializer(shop,many=False)
        return Response(shop_serializer.data)



class GlobelShopCategory(APIView):

    permission_classes = [CustomAdminPermission]

    def get(self, request, *args, **kwargs):
        product_category = ProductsCategorys.objects.filter(shop__isnull=True)
        if not product_category:
            return Response({'error':"NO Globel product category"})
        product_category_serializer = ProductCategorySerializer(product_category,many=True)
        return Response({"result":product_category_serializer.data})



class AddGlobelShopCategory(APIView):

    permission_classes = [CustomAdminPermission]

    def get(self, request, *args, **kwargs):
        return Response({"product_category_name":"required field","shop_category":"required field"})



    def post(self, request, *args, **kwargs):
        product_category_serializer = AddGlobelShopCategorySerializers(data=request.data)
        if product_category_serializer.is_valid(raise_exception=True):
            product_category_serializer.save()
            return Response({"result":product_category_serializer.data})



class EditGlobelShopCategory(APIView):

    permission_classes = [CustomAdminPermission]

    def get(self, request, *args, **kwargs):
        product_category_query = ProductsCategorys.objects.filter(id=kwargs["categoryid"])
        if not product_category_query:
            return Response({"error":"No Product category is exist"})
        product_category_serializer = ProductCategorySerializers(product_category_query,many=True)
        return Response({"result":product_category_serializer.data})


    def patch(self, request, *args, **kwargs):
        try:
            product_category_query = ProductsCategorys.objects.get(id=kwargs["categoryid"])
        except ProductsCategorys.DoesNotExist:
            return Response({"Error":'product category is not exist'})
        product_category_serializer = ProductCategorySerializers(product_category_query,data=request.data,many=False)
        if product_category_serializer.is_valid(raise_exception=True):
            product_category_serializer.save()
            return Response({'result':product_category_serializer.data})
    

    def delete(self, request, *args, **kwargs):
        try:
            ProductsCategorys.objects.get(id=kwargs['categoryid']).delete()
        except ProductsCategorys.DoesNotExist:
            return Response({"error":"product category is not exist"})
        return Response({"result":f"{kwargs['categoryid']} is deleted"})
