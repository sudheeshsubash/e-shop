from rest_framework import serializers
from .models import CustomUser,ShopCategorys
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

        validationerror = dict() # validation error variable
        # start validation here
        if len(username)<= 0 or len(password)<= 0:
            raise serializers.ValidationError('username and password required')

        if not re.match(r"^[a-zA-Z\s0-9]+$",password) or len(password) < 4 or len(password) > 20:
            validationerror['password2']={f"{password}":"Enter a valid password."}

        if not re.match(r"^[a-zA-Z\s]+$",username) or len(username) < 4 or len(username) > 20:
            validationerror['username']={f"{username}":'Enter a valid username.'}

        if len(validationerror) != 0:
            raise serializers.ValidationError(validationerror)
        return True
    


class MainCategoryShopCategorySerializer(serializers.ModelSerializer):
    '''
    
    '''
    class Meta:
        model = ShopCategorys
        fields = '__all__'
    
    def validate(self, attrs):
        shop_category_name,discribe = attrs.get('shop_category_name'),attrs.get('discribe')
        if not re.match(r"^[a-zA-Z\s]+$",shop_category_name):
            raise serializers.ValidationError({'validationerror':f'{shop_category_name} is not valid'})

        return attrs