from rest_framework.views import APIView
from .serializers import LoginSerializer,MainCategoryShopCategorySerializer,ShopRegistrationOtpSerializer
from django.contrib.auth import authenticate,login,logout
from .tokengeneratedecode import get_tokens_for_user,check_jwt_user_id_kwargs_id,get_decoded_payload,check_not_superadmin
from rest_framework.response import Response
from rest_framework import status
from .models import ShopDetails,ShopCategorys,ProductsCategorys
from .custompermissions import CustomAdminPermission
from rest_framework.decorators import permission_classes
from shopadmin.serializers import ShopCategoryOrMagerCategorySerializer,RegistrationShopDetailsSerializer,StaffRegistrationSerializer
from shopadmin.serializers import RegistrationShopDetailsOtpConfirmationSerializer,ProductCategorySerializer
from .serializers import AddGlobelShopCategorySerializers,ProductCategorySerializers
from superadmin.otps import otp
from django.contrib.auth.hashers import make_password
from .paginations import CustomPageNumberPagination




class LoginSuperAdminEndUserShopAdminShopStaff(APIView):
    '''
    this is login for all roles superadmin,
    eshopadmin, eshopstaff, enduser
    '''
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'status':'already login'},status=status.HTTP_208_ALREADY_REPORTED)
        login_serializer_data = LoginSerializer(request.data)
        if login_serializer_data.validate():
            username = login_serializer_data.data.get('username')
            password = login_serializer_data.data.get('password')
            print(type(username))
            users = authenticate(username=username,password=password)
            if users is not None:
                if users.is_superuser:
                    token = get_tokens_for_user(user=users)
                    login(request,users)
                    return Response({'token':token},status=status.HTTP_200_OK)
            return Response({'error':f'username and password is not correct'},status=status.HTTP_401_UNAUTHORIZED)
        


    @permission_classes([CustomAdminPermission])
    def delete(self, request):
        '''
        loogout
        '''
        if request.user.is_authenticated:
            logout(request=request)
            return Response({'logout successfuly'},status=status.HTTP_200_OK)
        return Response({'login':'pass the jwt token'},status=status.HTTP_204_NO_CONTENT)
        


class SuperAdminDashBord(APIView):
    '''
    superadmin dashbord graph
    '''
    permission_classes=[CustomAdminPermission]

    def get(self, request, *args, **kwargs):
        shop_category_query_list_result = dict()
        for shop_category_query in ShopCategorys.objects.all():
            shop_category_query_list_result[f"{shop_category_query.shop_category_name}"] = ShopDetails.objects.filter(shop_category=shop_category_query.id).count()
        return Response({"result":shop_category_query_list_result,"graph":"this graph is check how many user under the shopcategory"},status=status.HTTP_200_OK)



class ShopCategoryView(APIView):

    permission_classes = [CustomAdminPermission]

    def get(self, request, *args, **kwargs):
        pagination = CustomPageNumberPagination()
        try:
            shopcategory_from_database = ShopCategorys.objects.all()
        except ShopCategorys.DoesNotExist:
            return Response({'error':'No Shop categorys is exist'},status=status.HTTP_404_NOT_FOUND)
        query_page = pagination.paginate_queryset(shopcategory_from_database,request)
        return pagination.get_paginated_response(MainCategoryShopCategorySerializer(query_page,many=True).data)
    


class AddShopCategory(APIView):

    permission_classes = [CustomAdminPermission]

    def get(self, request, *args, **kwargs):
        return Response({"shop_category_name":'Enter the category name','discribe':'Discribe that category'},status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        category_serializer = MainCategoryShopCategorySerializer(data=request.data)
        if category_serializer.is_valid(raise_exception=True):
            category_serializer.save()
            category = Response(category_serializer.data).data
            return Response(category,status=status.HTTP_200_OK)



class EditShopCategory(APIView):

    permission_classes = [CustomAdminPermission]

    def get(self, request, *args, **kwargs):
        try:
            category_from_database = ShopCategorys.objects.get(id=kwargs['categoryid'])
        except ShopCategorys.DoesNotExist:
            return Response({'error':f'{kwargs["categoryid"]} is not valid '},status=status.HTTP_400_BAD_REQUEST)
        
        category_serializer = MainCategoryShopCategorySerializer(category_from_database)
        return Response({"result":category_serializer.data})
    

    def patch(self, request, *args, **kwargs):
        try:
            category_from_database = ShopCategorys.objects.get(id=kwargs['categoryid'])
        except ShopCategorys.DoesNotExist:
            return Response({'categoryid':f'{kwargs["categoryid"]} is not valid'},status=status.HTTP_404_NOT_FOUND)
        
        category_serializer = MainCategoryShopCategorySerializer(category_from_database,data=request.data)
        if category_serializer.is_valid(raise_exception=True):
            category_serializer.save()
            return Response({"result":category_serializer.data},status=status.HTTP_200_OK)
        
    
    def delete(self, request, *args, **kwargs):
        try:
            ShopCategorys.objects.get(id=kwargs['categoryid']).delete()
        except ShopCategorys.DoesNotExist:
            return Response({"error":"Category is not exist"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"result":"ShopCategory is deleted"},status=status.HTTP_200_OK)



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
        return Response({"result":result},status=status.HTTP_200_OK)


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

            return Response({"otp":f'otp sended to phone'},status=status.HTTP_200_OK)
            


class RegistrationOtpConfirm(APIView):
    '''
    
    '''
    def get(self, request):
        return Response({'result':{"otp":"required value"}})


    def post(self, request):
        otp_serializer = ShopRegistrationOtpSerializer(request.data)
        if int(otp_serializer.data.get('otp')) != request.session.get('otpnumber',None):
            return Response({'result':'otpnumber is not valid'},status=status.HTTP_200_OK)
        
        shopcategory = ShopCategorys.objects.get(id=request.session.get('shop_category'))
        
        shop = ShopDetails.objects.create(
                username = request.session.get('username'),
                password = make_password(request.session.get('password')),
                email = request.session.get('email'),
                place = request.session.get('place'),
                address = request.session.get('address'),
                ownername = request.session.get('ownername'),
                phone_number = request.session.get('phone_number'),
                shop_category = shopcategory,
                role = 'shopadmin',
        )
        request.session.flush()
        shop_serializer = RegistrationShopDetailsOtpConfirmationSerializer(shop,many=False)
        return Response({"result":shop_serializer.data},status=status.HTTP_200_OK)



class ShopsDetailsEdit(APIView):
    permission_classes = [CustomAdminPermission]
    def patch(self, request, *args, **kwargs):
        try:
            shop = ShopDetails.objects.get(id=kwargs['shopid'])
        except ShopDetails.DoesNotExist:
            return Response({"error":f"{kwargs['shopid']} is not valid"})
        if shop.is_active:
            shop.is_active = False
            shop.save()
            return Response({"result":f"{shop.username} is Block"})
        shop.is_active = True
        shop.save()
        return Response({"result":f"{shop.username} is UnBlock"})
    
    

    def delete(self, request, *args, **kwargs):
        try:
            ShopDetails.objects.get(id=kwargs['shopid']).delete()
        except ShopDetails.DoesNotExist:
            return Response({"error":f"{kwargs['shopid']} is not valid"})
        return Response({"result":"Shop is Deleted"})

    

class GlobelShopCategory(APIView):

    permission_classes = [CustomAdminPermission]

    def get(self, request, *args, **kwargs):
        shop = request.query_params.get('shop')
        if shop:
            product_category = ProductsCategorys.objects.filter(shop=shop)
            if not product_category:
                return Response({'error':"No Custom product category is available"},status=status.HTTP_400_BAD_REQUEST)
        else:
            product_category = ProductsCategorys.objects.filter(shop__isnull=True)
            if not product_category:
                return Response({'error':"NO Globel product category"},status=status.HTTP_400_BAD_REQUEST)
        product_category_serializer = ProductCategorySerializer(product_category,many=True)
        return Response({"result":product_category_serializer.data},status=status.HTTP_200_OK)



class AddGlobelShopCategory(APIView):

    permission_classes = [CustomAdminPermission]

    def get(self, request, *args, **kwargs):
        return Response({'result':{"product_category_name":"required field","shop_category":"required field"}},status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        product_category_serializer = AddGlobelShopCategorySerializers(data=request.data)
        if product_category_serializer.is_valid(raise_exception=True):
            product_category_serializer.save()
            return Response({"result":product_category_serializer.data},status=status.HTTP_200_OK)



class EditGlobelShopCategory(APIView):

    permission_classes = [CustomAdminPermission]

    def get(self, request, *args, **kwargs):
        product_category_query = ProductsCategorys.objects.filter(id=kwargs["categoryid"])
        if not product_category_query:
            return Response({"error":"No Product categorys is exist"},status=status.HTTP_400_BAD_REQUEST)
        product_category_serializer = ProductCategorySerializers(product_category_query,many=True)
        return Response({"result":product_category_serializer.data},status=status.HTTP_200_OK)


    def patch(self, request, *args, **kwargs):
        try:
            product_category_query = ProductsCategorys.objects.get(id=kwargs["categoryid"])
        except ProductsCategorys.DoesNotExist:
            return Response({"Error":'product category is not exist'},status=status.HTTP_400_BAD_REQUEST)
        product_category_serializer = ProductCategorySerializers(product_category_query,data=request.data,many=False)
        if product_category_serializer.is_valid(raise_exception=True):
            product_category_serializer.save()
            return Response({'result':product_category_serializer.data},status=status.HTTP_200_OK)
    

    def delete(self, request, *args, **kwargs):
        try:
            ProductsCategorys.objects.get(id=kwargs['categoryid']).delete()
        except ProductsCategorys.DoesNotExist:
            return Response({"error":"product category is not exist"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"result":f"{kwargs['categoryid']} is deleted"},status=status.HTTP_200_OK)
