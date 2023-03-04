from rest_framework.decorators import api_view,permission_classes
from .srializers import CustomSerializer,CustomLoginSerializer
from rest_framework.response import Response
from .models import CustomUser
from django.contrib.auth import authenticate
from .tokens_permissions import get_tokens_for_user,CustomAdminPermission
from rest_framework import status
from .paginations import CustomPageNumberPagination
from eshopadmin_app1.models import ShopDetails
from django.db.models import Q
from rest_framework.views import APIView


@api_view(['GET'])
@permission_classes([CustomAdminPermission])
def show_all_shops_users(request):
    '''
    admin can view all shops
    '''
    if request.method == 'GET':
        '''
        get jwt token to backend and decode that 
        then check the role and return Response
        '''
        pagination = CustomPageNumberPagination()
        user = CustomUser.objects.filter(Q(is_superuser=False)&Q(role='shopadmin'))
        result = pagination.paginate_queryset(user,request)
        serializer = CustomSerializer(result,many=True)
        return pagination.get_paginated_response(serializer.data)
    return Response({'msg':'You role is not valid for run this function'})
    


@api_view(['POST'])
def login(request):
    '''
    Admin login
    '''
    if request.method == 'POST':
        serializer = CustomLoginSerializer(request.data)
        if serializer.validate():
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                token = get_tokens_for_user(user=user)
                return Response({"token":token,"msg":"login success"},status=status.HTTP_200_OK)
        return Response({"msg":"username and passwor is not currect"},status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([CustomAdminPermission])
def block_shop(request,id):
    if request.method == 'GET':
        shop = ShopDetails.objects.get(id=id)
        shop.is_active = False
        shop.save()
        return Response({'msg':f'{shop} is blocked'})


@api_view(['GET'])
@permission_classes([CustomAdminPermission])
def un_block_shop(request,id):
    if request.method == 'GET':
        shop = ShopDetails.objects.get(id=id)
        shop.is_active = True
        shop.save()
        return Response({'msg':f'{shop} is unblocked'})



class ShopBlcokUnblock(APIView):
    '''
    
    '''
    # permission_classes=[CustomAdminPermission]

    def patch(self, request):
        shopid = request.query_params.get('sid')
        if shopid is None:
            return Response({'msg':'shopid is needed'})
        try:
            shop = ShopDetails.objects.get(id=shopid)
        except ShopDetails.DoesNotExist:
            return Response({'error':f'{shopid} is not valid'})
        
        if shop.is_active:
            shop.is_active=False
            shop.save()
            return Response({'response':f'{shop.username} is blocked'})
        shop.is_active=True
        shop.save()
        return Response({'response':f'{shop.username} is  Unblocked'})
