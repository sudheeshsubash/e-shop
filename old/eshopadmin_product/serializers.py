from rest_framework import serializers
from .models import ShopCategorys,ShopProducts,ProductImages
import re



class ShopCategorySerializers(serializers.ModelSerializer):
    '''
    add new data in shopcategory table
    '''
    class Meta:
        model = ShopCategorys
        fields = '__all__'
    
    def validate(self, attrs):
        category_name = attrs.get('category_name')
        if not re.match("^[a-zA-Z\s]+$",category_name):
            raise serializers.ValidationError('category is not valid')
        return attrs



class ShopProductSerializers(serializers.ModelSerializer):
    '''
    add new product in shoopproduct table
    '''
    class Meta:
        model = ShopProducts
        fields = [
            'name','price','stock','category_id'
        ]
    
    def save(self,shop_id):
        return ShopProducts.objects.create(
            name = self.data.get('name'),
            price = self.data.get('price'),
            stock = self.data.get('stock'),
            shop_id_id = shop_id,
            category_id_id = self.data.get('category_id')
        )

    def validate(self, attrs):
        return super().validate(attrs)




class UpdateShopProductDetails(serializers.ModelSerializer):
    '''
    update name price etc like 
    fields for shopproduct table
    '''
    class Meta:
        model = ShopProducts
        fields = [
            'name','price','stock','is_available',
            'category_id'
        ]


    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    



class AddProductImagesSerializer(serializers.Serializer):
    '''
    update images
    '''
    image = serializers.ListField(child=serializers.ImageField())

    def save(self, image, productid):
        
        return ProductImages.objects.create(
            image = image,
            product_id = productid.id
        )