from rest_framework import serializers
from superadmin.models import OrderProducts,EndUserOrders,ShopStaff,CustomUser
import re


class StaffViewOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndUserOrders
        fields = ['id','payment_type','create','total_amount']
    


class OrderProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = ['product_name','product_price','quantity','total']



class ChangeStatusSerializer(serializers.ModelSerializer):
    # payment = serializers.IntegerField()
    # payment_type = serializers.CharField(max_length=50)
    class Meta:
        model = EndUserOrders
        fields = ['order_status','payment_credit','payment_debit']

    def save(self, **kwargs):
        order = EndUserOrders.objects.get(id=kwargs['orderid'])
        staff = ShopStaff.objects.get(id=kwargs['staffid'])
        order.staff_id = staff.id
        order.payment_credit = self.data.get('payment_credit')
        # order.payment_debit = self.data.get('payment_debit')
        order.order_status = self.data.get("order_status")
        print(self.data.get("order_status"))
        order.save()
        return order



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