from rest_framework import serializers
from superadmin.models import OrderProducts,EndUserOrders



class StaffViewOrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndUserOrders
        fields = ['id','payment_type','create','total_amount']
    


class OrderProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = ['product_name','product_price','quantity','total']



class ChangeStatusSerializer(serializers.ModelSerializer):
    payment = serializers.IntegerField()