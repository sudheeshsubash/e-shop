from rest_framework import serializers
from .models import CustomUser
import re



class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'username','password'
        ]

    def validate(self):
        username = self.data.get('username')
        password = self.data.get('password')
        print(username,password)
        if len(username)<= 0 or len(password)<= 0:
            raise serializers.ValidationError('username and password required')
        if (len(username) <  4 or len(username) > 20):
            raise serializers.ValidationError('not valid username only 5 to 20 character allowed')
        if (len(password) > 20 or len(password)< 4):
            raise serializers.ValidationError('not valid password,it is between 4 to 20')
        
        return True
    