from superadmin.models import ProductReview,CustomUser,ShopProducts,ShopDetails,UsersDetails
from rest_framework import serializers


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['message','rate']
    
