from rest_framework import serializers
from superadmin.models import OrderProducts,EndUserOrders,ShopStaff
import re


class StaffViewOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndUserOrders
        fields = ['id','payment_type','create','total_amount']
    


class OrderProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = ['product_name','product_price','quantity','total']



class ChangeStatusSerializer(serializers.Serializer):

    payment = serializers.IntegerField()
    payment_type = serializers.CharField(max_length=50)



class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopStaff
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

        if not re.match(r"^[a-zA-Z0-9\s]+$",username) or len(username) < 4 or len(username) > 20:
            validationerror['username']={f"{username}":'Enter a valid username.'}

        if len(validationerror) != 0:
            raise serializers.ValidationError(validationerror)
        return True