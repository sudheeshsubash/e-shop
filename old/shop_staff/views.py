from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import LoginShopStaffSerializers
from admin_app1.tokens_permissions import get_tokens_for_user
from django.contrib.auth import authenticate




@api_view(['POST'])
def shop_staff_login(request):
    if request.method == 'POST':
        shopstaffserializer = LoginShopStaffSerializers(request.data)
        if shopstaffserializer.validate():
            shopstaff = authenticate(username=shopstaffserializer.data.get('username'),password=shopstaffserializer.data.get('password'))
            if shopstaff is not None:
                token = get_tokens_for_user(user=shopstaff)
                return Response({'token':token})
            return Response({"error":'shop staff is not valid'})
        return Response({"error":"data is not valid"})


