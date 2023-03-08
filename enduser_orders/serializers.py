from rest_framework import serializers
from .models import EndUserOrders,OrderProducts
from admin_app1.models import CustomUser


class OrderPlaceSerializer(serializers.ModelSerializer):
    '''
    enduserorder
    '''
    class Meta:
        model=EndUserOrders
        fields=''




class OrderProductSerializer(serializers.ModelSerializer):
    '''
    orderproducts
    '''
    class Meta:
        model=OrderProducts
        fields=''



class ViewEndUserOrdersSerializer(serializers.ModelSerializer):
    '''
    
    '''
    class Meta:
        model=CustomUser
        fields=''
