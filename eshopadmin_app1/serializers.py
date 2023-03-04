from .models import ShopDetails,ShopStaff
from admin_app1.models import CustomUser
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
import re

class ShopDetailsRegisterSerializer(serializers.ModelSerializer):
    '''
    shopdetails add new data
    '''
    class Meta:
        model = ShopDetails
        fields = [
            'username','password','email',
            'place','address','ownername',
            'phone_number'
        ]

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        phone_number = attrs.get("phone_number")
        email = attrs.get('email')
        place = attrs.get('place')
        address = attrs.get('address')
        ownername = attrs.get('ownername')
        if len(str(phone_number))!=10:
            raise serializers.ValidationError("phone number is not valid")
        if not re.match("^[a-zA-Z]+$",username) or len(username)<4 or len(username)>20:
            raise serializers.ValidationError('User Name is not valid')
        if not re.match("^[a-zA-Z0-9]+$",password) or len(password)<4 or len(password)>20:
            raise serializers.ValidationError('password is not valid')
        if not re.match("^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,3})$",email):
            raise serializers.ValidationError('email is not valid')
        if not re.match("^[a-zA-Z]+$",place) or len(place)<4 or len(place)>22:
            raise serializers.ValidationError('place is not valid')
        if not re.match('^[a-zA-Z\s]+$',address):
            raise serializers.ValidationError('address is not valid')
        if not re.match('^[a-zA-z]+$',ownername) or len(ownername)<3 or len(ownername)>20:
            raise serializers.ValidationError('owner name is not valid')
        return attrs
    

class ShopDetailsLoginSerializer(serializers.ModelSerializer):
    '''
    shop details data authenticate and validate
    '''
    class Meta:
        model = ShopDetails
        fields = ['username','password']

    def validate(self):
        username = self.data.get('username')
        password = self.data.get('password')
        if not re.match("^[a-zA-Z]+$",username) or len(username)<4 or len(username)>20:
            raise serializers.ValidationError('User Name is not valid')
        if not re.match('^[a-zA-Z0-9]+$',password) or len(password) <4 or len(password)>20:
            raise serializers.ValidationError('password is not valid')
        return True



class CreateShopStaffSerializer(serializers.ModelSerializer):
    '''
    shop details data authenticate and validate
    '''
    class Meta:
        model = ShopStaff
        fields = ['username','password','phone_number']

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        phone_number = attrs.get('phone_number')
        if not re.match("^[a-zA-Z\s]+$",username) or len(username)<4 or len(username)>20:
            raise serializers.ValidationError('User Name is not valid only [a-z,A-Z," "]')
        if not re.match('^[a-zA-Z0-9]+$',password) or len(password) <4 or len(password)>20:
            raise serializers.ValidationError('password is not valid only [a-z ,A-Z, 0-9]')
        if len(str(phone_number)) != 10:
            raise serializers.ValidationError('Phone Number is not valid')
        return attrs

    def save(self,shop_id):
        

        return ShopStaff.objects.create(
            username = self.data.get('username'),
            password = make_password(self.data.get('password')),
            phone_number = self.data.get('phone_number'),
            shop_id_id = int(shop_id),
            role = 'shopstaff'
        )

    