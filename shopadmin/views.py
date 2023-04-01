from rest_framework.views import APIView
from rest_framework.response import Response
from superadmin.tokengeneratedecode import get_decoded_payload,get_tokens_for_user,check_jwt_user_id_kwargs_id
from superadmin.custompermissions import CustomShopAdminPermission
from .serializers import ShopCategoryOrMagerCategorySerializer,RegistrationShopDetailsSerializer,EditProductCategorySerializer,ShopStaffSerializer
from .serializers import RegistrationShopDetailsOtpConfirmationSerializer,ProductCategorySerializer,AddProductCategorySerializer,StaffRegistrationSerializer
from superadmin.models import ShopCategorys,ShopDetails,ProductsCategorys,ShopStaff,CustomUser
from superadmin.otps import otp
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from superadmin.serializers import LoginSerializer
from django.contrib.auth import authenticate,login,logout
from rest_framework import status



class StaffRegistrationView(APIView):

    permission_classes = [CustomShopAdminPermission]

    def post(self, request, *args, **kwargs):
        registration_form_data = StaffRegistrationSerializer(data=request.data)
        if registration_form_data.is_valid(raise_exception=True):
            staff_query = registration_form_data.save()
            staff = CustomUser.objects.get(username=staff_query)
            print(staff.id)
            # ShopStaff.objects.create(
            #     shop = staff_query.id
            # )
            return Response({"result":"New staff created"},status=status.HTTP_201_CREATED)


class ShopStaffView(APIView):

    permission_classes = [CustomShopAdminPermission]

    def get(self, request, *args, **kwargs):
        shop_staff_query = ShopStaff.objects.filter(shop=kwargs['shopid'])
        shop_serializer = ShopStaffSerializer(shop_staff_query,many=True)
        return Response({"result":shop_serializer.data})



class ShopStaffEdit(APIView):

    permission_classes = [CustomShopAdminPermission]

    def patch(self, request, *args, **kwargs):
        try:
            shop_details = ShopStaff.objects.get(id=kwargs['staffid'])
        except ShopStaff.DoesNotExist:
            return Response({"error":"staff is not exist"})
        if shop_details.is_active:
            shop_details.is_active = False
            shop_details.save()
            return Response({"result":f"{shop_details.username} is blocked"})
        shop_details.is_active=True
        shop_details.save()
        return Response({'result':f"{shop_details.username} is unblocked"})


    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        try:
            ShopStaff.objects.get(id=kwargs['staffid']).delete()
        except ShopStaff.DoesNotExist:
            return Response({"error":f"{kwargs['staffid']} is not valid"},status=status.HTTP_400_BAD_REQUEST)
        return Response({"result":"Shop staff details deleted"},status=status.HTTP_200_OK)



class ShopAdminDashBord(APIView):
    '''
    shop admin dashbord
    '''
    permission_classes=[CustomShopAdminPermission]
    
    def get(self, request, *args, **kwargs):
        if check_jwt_user_id_kwargs_id(request,kwargs['shopid']):
            return Response({"result":'shop admin dashbord'},status=status.HTTP_200_OK)
        return Response({'error':'You dont have permission for access this api'},status=status.HTTP_400_BAD_REQUEST)



class ShopAdminLogin(APIView):
    '''
    shop admin login
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
            return Response({'error':f'username and password is not correct'},status=status.HTTP_401_UNAUTHORIZED)



class ViewAllProductCategoryGlobelAndCustomCategorys(APIView):
    '''
    this is show all globel and custom categorys
    '''
    permission_classes=[CustomShopAdminPermission]

    def get(self, request, *args, **kwargs):
        if not check_jwt_user_id_kwargs_id(request,kwargs['shopid']):
            return Response({'error':"You have no permission for access this shop method"},status=status.HTTP_400_BAD_REQUEST)
        product_category_query = ProductsCategorys.objects.filter(Q(shop__isnull=True)|Q(shop=kwargs['shopid']))
        if not product_category_query:
            return Response({'error':f'No Products Category, is empty'},status=status.HTTP_400_BAD_REQUEST)
        
        product_category_serializer = ProductCategorySerializer(product_category_query,many=True)
        return Response({"result":product_category_serializer.data},status=status.HTTP_200_OK)



class ProductCategoryEdit(APIView):

    permission_classes = [CustomShopAdminPermission]

    def get(self, request, *args, **kwargs):

        if not check_jwt_user_id_kwargs_id(request,kwargs['shopid']):
            return Response({'error':"You have no permission for access this shop method"},status=status.HTTP_400_BAD_REQUEST)
        product_category_query = ProductsCategorys.objects.filter(id=kwargs['categoryid'],shop=kwargs['shopid']).values('product_category_name')
        if not product_category_query:
            return Response({'error':f'{kwargs["categoryid"]} is not valid'},status=status.HTTP_400_BAD_REQUEST)
        product_category_serializer = EditProductCategorySerializer(product_category_query,many=True)
        return Response({"result":product_category_serializer.data},status=status.HTTP_200_OK)



    def patch(self, request, *args, **kwargs):
        
        if not check_jwt_user_id_kwargs_id(request,kwargs['shopid']):
            return Response({'error':"You have no permission for access this shop method"},status=status.HTTP_400_BAD_REQUEST)
        try:
            customize_product_category_query = ProductsCategorys.objects.get(id=kwargs['categoryid'],shop=kwargs['shopid'])
        except ProductsCategorys.DoesNotExist:
            return Response({'error':f'{kwargs["categoryid"]} is not valid'},status=status.HTTP_400_BAD_REQUEST)
        product_category_serializer = EditProductCategorySerializer(customize_product_category_query,data=request.data)
        if product_category_serializer.is_valid(raise_exception=True):
            product_category_serializer.save()
            return Response({"result":product_category_serializer.data},status=status.HTTP_200_OK)
        return Response({"error":'Enter a valid credetials'},status=status.HTTP_400_BAD_REQUEST)
    


    def delete(self, request, *args, **kwargs):
        try:
            ProductsCategorys.objects.get(id=kwargs['categoryid']).delete()
        except ProductsCategorys.DoesNotExist:
            return Response({'error':'category Not exist'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':"category is deleted"},status=status.HTTP_200_OK)



class ProductCategoryAdd(APIView):

    permission_classes = [CustomShopAdminPermission]

    def get(self, request, *args, **kwargs):

        if not check_jwt_user_id_kwargs_id(request,kwargs['shopid']):
            return Response({'error':"You have no permission for access this shop method"},status=status.HTTP_400_BAD_REQUEST)
        return Response({'result':{'required field':'product_category_name'}},status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        
        if not check_jwt_user_id_kwargs_id(request,kwargs['shopid']):
            return Response({'error':"You have no permission for access this shop method"},status=status.HTTP_400_BAD_REQUEST)
        try:
            shop_details = ShopDetails.objects.get(id=kwargs['shopid'])
        except ShopDetails.DoesNotExist:
            return Response({'error':'shop is not valid'},status=status.HTTP_400_BAD_REQUEST)
        product_category_serializer = AddProductCategorySerializer(data=request.data)
        if product_category_serializer.is_valid(raise_exception=True):
            custom_product_category = ProductsCategorys.objects.create(
                product_category_name = product_category_serializer.data.get('product_category_name'),
                shop=shop_details,shop_category=shop_details.shop_category
            )
            custom_product_category_serializer = ProductCategorySerializer(custom_product_category)
            return Response({"result":custom_product_category_serializer.data},status=status.HTTP_200_OK)
