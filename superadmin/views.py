from rest_framework.views import APIView
from .serializers import LoginSerializer,MainCategoryShopCategorySerializer
from django.contrib.auth import authenticate,login,logout
from .tokengeneratedecode import get_tokens_for_user
from rest_framework.response import Response
from rest_framework import status
from .models import ShopDetails,ShopCategorys
from .custompermissions import CustomAdminPermission
from rest_framework.decorators import permission_classes



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
    def patch(self, request):
        shopid = request.query_params.get('shopid')
        if shopid is None:
            return Response({'msg':'shopid is needed'})
        try:
            shop_query = ShopDetails.objects.get(id=shopid)
        except ShopDetails.DoesNotExist:
            return Response({'error':f'{shopid} is not valid'},status=status.HTTP_400_BAD_REQUEST)
        
        if shop_query.is_active:
            shop_query.is_active=False
            shop_query.save()
            return Response({'response':f'{shop_query.username} is blocked'},status=status.HTTP_200_OK)
        shop_query.is_active=True
        shop_query.save()
        return Response({'response':f'{shop_query.username} is  Unblocked'},status=status.HTTP_200_OK)




class ShopCategoryOrMainClassification(APIView):
    '''
    this category is the main category of shop and everything
    '''
    permission_classes=[CustomAdminPermission]
    def get(self, request):
        try:
            shopcategory_from_database = ShopCategorys.objects.all()
        except ShopCategorys.DoesNotExist:
            return Response({'error':'no main categorys'})
        
        shopcategory_serializer = MainCategoryShopCategorySerializer(shopcategory_from_database,many=True)
        return Response(shopcategory_serializer.data)




class CustomizeShopCategoryOrMainCategory(APIView):
    '''
    this api is give add category and edit category
    '''
    permission_classes = [CustomAdminPermission]

    def get(self, request):
        method_type = request.query_params.get('type')
        if method_type is None:
            return Response({'query params have ?type=add (or) edit'})
        
        if method_type == 'add':
            return Response({"shop_category_name":'Enter the category name','discribe':'Discribe that category'})

        if method_type != 'edit':
            return Response({'type value is not valid only add and edit is expected'})
        
        category_id = request.query_params.get('categoryid')
        if category_id is None:
            return Response({"categoryid":'query param (categoryid) is needed'})
        try:
            category_from_database = ShopCategorys.objects.get(id=category_id)
        except ShopCategorys.DoesNotExist:
            return Response({'error':f'{category_id} is not valid or (categoryi)d is not valid'})
        
        category_serializer = MainCategoryShopCategorySerializer(category_from_database)
        return Response(category_serializer.data)
    


    def post(self, request):
        method_type = request.query_params.get('type')
        if method_type is None:
            return Response({'query params have ?type=add'})
        
        if method_type != 'add':
            return Response({"shop_category_name":'Enter the category name','discribe':'Discribe that category'})

        category_serializer = MainCategoryShopCategorySerializer(data=request.data)
        if category_serializer.is_valid(raise_exception=True):
            category_serializer.save()
            category = Response(category_serializer.data).data
            return Response(category)
        


    def patch(self, request):
        method_type = request.query_params.get('type')
        category_id = request.query_params.get('categoryid')

        if method_type is None:
            return Response({'query params have ?type=edit'})
        
        if method_type != 'edit':
            return Response({'type value is not valid only add and edit is expected'})
        
        if category_id is None:
            return Response({'query param':'query parm needed (categoryid)'})
        try:
            category_from_database = ShopCategorys.objects.get(id=category_id)
        except ShopCategorys.DoesNotExist:
            return Response({'categoryid':f'{category_id} is not valid'})
        
        category_serializer = MainCategoryShopCategorySerializer(category_from_database,data=request.data)
        if category_serializer.is_valid(raise_exception=True):
            category_serializer.save()
            return Response(category_serializer.data)