from eshopadmin_app1.models import ShopStaff
from rest_framework import serializers
import re


class LoginShopStaffSerializers(serializers.ModelSerializer):

    class Meta:
        model = ShopStaff
        fields = ['username','password']

    def validate(self):
        username = self.data.get('username')
        password = self.data.get('password')
        if not re.match("^[a-zA-Z]+$",username) or len(username)<4 or len(username)>20:
            raise serializers.ValidationError('User Name is not valid')
        if not re.match('^[a-zA-Z0-9]+$',password) or len(password) <4 or len(password)>20:
            raise serializers.ValidationError('password is not valid')
        return True