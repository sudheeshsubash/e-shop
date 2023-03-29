from rest_framework.views import APIView
from rest_framework.response import Response
from superadmin.tokengeneratedecode import get_decoded_payload,get_tokens_for_user,check_jwt_user_id_kwargs_id
from superadmin.custompermissions import CustomShopAdminPermission
from .serializers import ShopCategoryOrMagerCategorySerializer,RegistrationShopDetailsSerializer,EditProductCategorySerializer
from .serializers import RegistrationShopDetailsOtpConfirmationSerializer,ProductCategorySerializer,AddProductCategorySerializer,StaffRegistrationSerializer
from superadmin.models import ShopCategorys,ShopDetails,ProductsCategorys,ShopStaff,CustomUser
from superadmin.otps import otp
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from superadmin.serializers import LoginSerializer
from django.contrib.auth import authenticate,login,logout
from rest_framework import status




class StaffRegistration(APIView):
    def post(self, request):
        registration_form_data_serializer = StaffRegistrationSerializer(data=request.data)
        if registration_form_data_serializer.is_valid(raise_exception=True):
            if registration_form_data_serializer.data.get('password') != registration_form_data_serializer.data.get('password2'):
                return Response({"error":"password is not valid"})
            staffdetails = CustomUser.objects.create(
                username = registration_form_data_serializer.data.get('username'),
                password = registration_form_data_serializer.data.get('password'),
                phone_number = registration_form_data_serializer.data.get('phone_number'),
                role = 'shopstaff',
            )
            ShopStaff.objects.create(
                shop_id = staffdetails.id
            )
            return Response({"result":"new staff registed"})




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



class ProductCategoryEdit(APIView):

    permission_classes = [CustomShopAdminPermission]

    def get(self, request, *args, **kwargs):

        if not check_jwt_user_id_kwargs_id(request,kwargs['shopid']):
            return Response({'error':"You have no permission for access this shop method"})

        try:
            product_category_query = ProductsCategorys.objects.filter(id=kwargs['categoryid'],shop=kwargs['shopid']).values('product_category_name')
        except ProductsCategorys.DoesNotExist:
            return Response({'error':'No exist Product categorys'})
        
        product_category_serializer = EditProductCategorySerializer(product_category_query,many=True)
        return Response(product_category_serializer.data)


    def patch(self, request, *args, **kwargs):
        
        if not check_jwt_user_id_kwargs_id(request,kwargs['shopid']):
            return Response({'error':"You have no permission for access this shop method"})

        try:
            customize_product_category_query = ProductsCategorys.objects.get(id=kwargs['categoryid'],shop=kwargs['shopid'])
        except ProductsCategorys.DoesNotExist:
            return Response({'error':f'{kwargs["categoryid"]} is not valid'})
        
        product_category_serializer = EditProductCategorySerializer(customize_product_category_query,data=request.data)
        if product_category_serializer.is_valid(raise_exception=True):
            product_category_serializer.save()
            return Response(product_category_serializer.data)
        return Response({"error":'Enter a valid credetials'})
    

    def delete(self, request, *args, **kwargs):
        try:
            ProductsCategorys.objects.get(id=kwargs['categoryid']).delete()
        except ProductsCategorys.DoesNotExist:
            return Response({'error':'category Not exist'})
        return Response({'result':"category is deleted"})


class ProductCategoryAdd(APIView):

    def get(self, request, *args, **kwargs):

        if not check_jwt_user_id_kwargs_id(request,kwargs['shopid']):
            return Response({'error':"You have no permission for access this shop method"})

        return Response({'product_category_name':'required field'})


    def post(self, request, *args, **kwargs):
        
        if not check_jwt_user_id_kwargs_id(request,kwargs['shopid']):
            return Response({'error':"You have no permission for access this shop method"})

        try:
            shop_details = ShopDetails.objects.get(id=kwargs['shopid'])
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
        






#     # def get(self, request):
#     #     takeshopid_from_token = get_decoded_payload(request)
#     #     try:
#     #         product_category_query = ProductsCategorys.objects.filter(Q(shop__isnull=True)|Q(shop=takeshopid_from_token['user_id']))
#     #     except ProductsCategorys.DoesNotExist:
#     #         return Response({'error':'No Product categorys'})
        
#     #     product_category_serializer = ProductCategorySerializer(product_category_query,many=True)
#     #     return Response(product_category_serializer.data)



# class CustomizeProductCategoryOrEditAddCategory(APIView):
#     '''
#     this is possible for (Add,Edit)(GET,POST,PATCH) methods
#     '''
#     permission_classes = [CustomShopAdminPermission]

#     def get(self, request, *args, **kwargs):

#         if kwargs['type'] == 'add':
#            return Response({'result':'required form field, Enter the value "product_category_name"'})

#         if kwargs['type'] != 'edit':
#             return Response({'not valid type'})
        
#         custom_product_category_id = request.query_params.get('categoryid')
#         takeshopid_from_token = get_decoded_payload(request)
#         if custom_product_category_id is None:
#             return  Response({'pass (categoryid) in query param'})
#         try:
#             product_category_query = ProductsCategorys.objects.filter(id=custom_product_category_id,shop=takeshopid_from_token['user_id']).values('product_category_name')
#         except ProductsCategorys.DoesNotExist:
#             return Response({'error':'No exist Product categorys'})
        
#         product_category_serializer = EditProductCategorySerializer(product_category_query,many=True)
#         return Response(product_category_serializer.data)



#     # def get(self, request):
#     #     customize_type = request.query_params.get('type')
#     #     if customize_type is None:
#     #         return Response({'pass query param value like ?type=add (or) edit'})
        
#     #     if customize_type == 'add':
#     #         return Response({'result':'required form field, Enter the value "product_category_name"'})
        
#     #     if customize_type != 'edit':
#     #         return Response({'not valid type'})
        
#     #     custom_product_category_id = request.query_params.get('categoryid')
#     #     takeshopid_from_token = get_decoded_payload(request)
#     #     if custom_product_category_id is None:
#     #         return  Response({'pass (categoryid) in query param'})
#     #     try:
#     #         product_category_query = ProductsCategorys.objects.filter(id=custom_product_category_id,shop=takeshopid_from_token['user_id']).values('product_category_name')
#     #     except ProductsCategorys.DoesNotExist:
#     #         return Response({'error':'No exist Product categorys'})
        
#     #     product_category_serializer = EditProductCategorySerializer(product_category_query,many=True)
#     #     return Response(product_category_serializer.data)
        

#     def post(self, request, *args, **kwargs):
#         if kwargs['type'] != 'add':
#             Response({'error':'api error'})
#         try:
#             shop_details = ShopDetails.objects.get(id=kwargs['shopid'])
#         except ShopDetails.DoesNotExist:
#             return Response({'error':'shop is not valid'})
        
#         product_category_serializer = AddProductCategorySerializer(data=request.data)
#         if product_category_serializer.is_valid(raise_exception=True):
#             custom_product_category = ProductsCategorys.objects.create(
#                 product_category_name = product_category_serializer.data.get('product_category_name'),
#                 shop=shop_details,shop_category=shop_details.shop_category
#             )
#             custom_product_category_serializer = ProductCategorySerializer(custom_product_category)
#             return Response(custom_product_category_serializer.data)

    

#     # def post(self, request):
#     #     customize_type = request.query_params.get('type')
#     #     if customize_type is None:
#     #         return Response({'pass query param value like ?type=add'})
        
#     #     if customize_type != 'add':
#     #         return Response({'only ?type=add is valid of post method'})
        
#     #     takeshopid_from_token = get_decoded_payload(request)

        
#     #     try:
#     #         shop_details = ShopDetails.objects.get(id=takeshopid_from_token['user_id'])
#     #     except ShopDetails.DoesNotExist:
#     #         return Response({'error':'shop is not valid'})
        
#     #     product_category_serializer = AddProductCategorySerializer(data=request.data)
#     #     if product_category_serializer.is_valid(raise_exception=True):
#     #         custom_product_category = ProductsCategorys.objects.create(
#     #             product_category_name = product_category_serializer.data.get('product_category_name'),
#     #             shop=shop_details,shop_category=shop_details.shop_category
#     #         )
#     #         custom_product_category_serializer = ProductCategorySerializer(custom_product_category)
#     #         return Response(custom_product_category_serializer.data)



#     # def patch(self, request):
#     #     customize_type = request.query_params.get('type')
#     #     product_category_id = request.query_params.get('productid')
#     #     takeshopid_from_token = get_decoded_payload(request)

#     #     if customize_type is None or product_category_id is None:
#     #         return Response({'result':'pass (type) and (productid) to query params'})
#     #     if customize_type != 'edit':
#     #         return Response({'result':'only ?type=edit is valid'})
        
#     #     try:
#     #         customize_product_category_query = ProductsCategorys.objects.get(id=product_category_id,shop=takeshopid_from_token['user_id'])
#     #     except ProductsCategorys.DoesNotExist:
#     #         return Response({'error':f'{product_category_id} is not valid'})
        
#     #     product_category_serializer = EditProductCategorySerializer(customize_product_category_query,data=request.data)
#     #     if product_category_serializer.is_valid(raise_exception=True):
#     #         product_category_serializer.save()
#     #         return Response(product_category_serializer.data)
#     #     return Response({"error":'Enter a valid credetials'})
    
    
#     def patch(self, request, *args, **kwargs):
#         product_category_id = request.query_params.get('productid')
#         if product_category_id is None:
#             return Response({'result':'pass (?productid=value) to query params'})
#         if kwargs['type'] != 'edit':
#             return Response({'error':'api error'})
        
#         try:
#             customize_product_category_query = ProductsCategorys.objects.get(id=product_category_id,shop=kwargs['shopid'])
#         except ProductsCategorys.DoesNotExist:
#             return Response({'error':f'{product_category_id} is not valid'})
        
#         product_category_serializer = EditProductCategorySerializer(customize_product_category_query,data=request.data)
#         if product_category_serializer.is_valid(raise_exception=True):
#             product_category_serializer.save()
#             return Response(product_category_serializer.data)
#         return Response({"error":'Enter a valid credetials'})
