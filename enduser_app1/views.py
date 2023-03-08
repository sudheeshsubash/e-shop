from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from .serializers import EndUserRegistrationSerializers,EndUserLoginSerializer,EndUserViewShop,EndUserDetailsEditSerializer,EndUserEditPasswordSerializer
from admin_app1.otp import otp
from admin_app1.models import CustomUser
from eshopadmin_app1.models import ShopDetails
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from admin_app1.tokens_permissions import get_tokens_for_user,CustomEndUserPermission
from rest_framework import filters
from django_filters import rest_framework as filters
from admin_app1.paginations import CustomPageNumberPagination
from eshopadmin_product.models import ShopProducts
from rest_framework.views import APIView




@api_view(['POST','GET'])
def register_new_end_user(request):
    '''
    register(sign in) end user
    add new user role to database
    '''
    if request.method == 'POST':
        enduserserializer = EndUserRegistrationSerializers(data=request.data)
        if enduserserializer.is_valid(raise_exception=True):
            otpnumber = otp(phone=enduserserializer.data.get('phone_number'))

            request.session['phone_number'] = enduserserializer.data.get('phone_number')
            request.session['username'] = enduserserializer.data.get('username')
            request.session['password'] = enduserserializer.data.get('password')
            request.session['otpnumber'] = otpnumber()

            return Response({"msg":"otp send current phone number"})
        return Response({"error":"credentials is not valid"})
    

    if request.method == 'GET':
        if 'otpnumber' in request.session:
            query_otp = request.query_params
            print(f"type of otp{type(query_otp.get('otp'))},session type {type(request.session['otpnumber'])}")
            if int(query_otp.get('otp'))==request.session['otpnumber']:
                enduser = CustomUser.objects.create(
                    username = request.session['username'],
                    phone_number = request.session['phone_number'],
                    password = make_password(request.session['password']),
                    role = 'enduser'
                )
                request.session.flush()
                return Response({'msg':f'{enduser.username} created'})
            return Response({'msg':"otp is not match try again"})
        return Response({'msg':'you canot run this request now'})
    



@api_view(['POST'])
def login_end_user(request):
    '''
    login enduser here generate enduser role base 
    token and shop base token
    '''
    loginserializer = EndUserLoginSerializer(request.data)
    if loginserializer.validate():
        enduser = authenticate(username=loginserializer.data.get('username'),password=loginserializer.data.get('password'))
        if enduser is not None:
            token = get_tokens_for_user(user=enduser)
            return Response({'token':token,'msg':'enduser login success'})
        return Response({'error':'you cant login right now','msg':'user credentials is not valid'})



class UserFilter(filters.FilterSet):
    '''
    eshop detail filtering class
    '''
    class Meta:
        model = ShopDetails
        fields = ['username','place']




class ViewAllShopsDetails(APIView):
    '''
    view all shop details and select shop
    '''
    permission_classes=[CustomEndUserPermission]

    def get(self, request):
        pagination = CustomPageNumberPagination()
        user_queryset = ShopDetails.objects.all()
        user_filter = UserFilter(request.query_params, queryset=user_queryset)
        result = pagination.paginate_queryset(user_filter.qs,request)
        serializer = EndUserViewShop(result, many=True)
        return pagination.get_paginated_response(serializer.data)




class EditDetailsOfEndUser(APIView):
    '''
    
    '''

    def patch(self, request):
        user_id = request.query_params.get('userid')
        if user_id is None:
            return Response({"error":'pass query params (userid)'})
        try:
            userdetails = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'msg':f'{user_id} is not valid'})
        enduserdetailsserializer = EndUserDetailsEditSerializer(userdetails,data=request.data)
        if enduserdetailsserializer.is_valid(raise_exception=True):
            enduserdetailsserializer.save()
            return Response(enduserdetailsserializer.data)
        return Response({'msg':'data not valid'})
    


    def put(self, request):
        user_id = request.query_params.get('userid')
        if user_id is None:
            return Response({"error":'pass query params (userid)'})
        try:
            userdetails = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({'msg':f'{user_id} is not valid'})
        enduserdetailsserializer = EndUserEditPasswordSerializer(userdetails,data=request.data)
        if enduserdetailsserializer.is_valid(raise_exception=True):
            enduserdetailsserializer.save()
            return Response(enduserdetailsserializer.data)
        return Response({'msg':'data not valid'})
    
