from admin_app1.models import CustomUser
from eshopadmin_app1.models import ShopDetails
from eshopadmin_product.models import ShopProducts
from rest_framework import serializers
import re
from django.contrib.auth.hashers import make_password


class EndUserRegistrationSerializers(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username','password','phone_number']
    
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        phone_number = attrs.get("phone_number")
        if len(str(phone_number))!=10:
            raise serializers.ValidationError("phone number is not valid")
        if not re.match("^[a-zA-Z]+$",username) or len(username)<4 or len(username)>20:
            raise serializers.ValidationError('User Name is not valid')
        if not re.match("^[a-zA-Z0-9]+$",password) or len(password)<4 or len(password)>20:
            raise serializers.ValidationError('password is not valid')
        return attrs
    


class EndUserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['username','password']

    def validate(self):
        username = self.data.get('username')
        password = self.data.get('password')
        if len(username)<= 0 or len(password)<= 0:
            raise serializers.ValidationError('username and password required')
        if not re.match("^[a-zA-Z]+$",username) or len(username)<4 or len(username)>20:
            raise serializers.ValidationError('User Name is not valid')
        if not re.match('^[a-zA-Z0-9]+$',password) or len(password) <4 or len(password)>20:
            raise serializers.ValidationError('password is not valid')
        return True
    


class EndUserViewShop(serializers.ModelSerializer):
    class Meta:
        model = ShopDetails
        fields = '__all__'



class EndUserDetailsEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','phone_number']


class EndUserEditPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['password']

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance