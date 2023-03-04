from rest_framework import serializers
from .models import EndUserOrders,OrderProducts



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
