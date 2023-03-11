from rest_framework import serializers
from superadmin.models import ProductVariation,ProductsCategorys,ShopProducts,ProductImages,CustomUser
import re
from django.db.models import Q



class ProductVariationSerializer(serializers.ModelSerializer):
    '''
    
    '''
    class Meta:
        model = ProductVariation
        fields = ['id','variation_name',]

    

class ProductCategorySerializer(serializers.ModelSerializer):
    '''
    
    '''
    class Meta:
        model = ProductsCategorys
        fields = ['id','product_category_name',]



class AddShopProductSerializer(serializers.ModelSerializer):
    '''
    
    '''
    image = serializers.ListField(child=serializers.ImageField())

    class Meta:
        model = ShopProducts
        fields = [
            'name','price','stock','discription',
            'categoryid','variation','image'
        ]
    
    def validate(self, attrs):

        validation_error = dict()
        if not re.match(r"^[a-zA-Z]+[a-zA-Z\s0-9]+$",attrs.get('name')):
            validation_error['name']=f"Enter a valid name. This value may contain a-z,A-Z,0-9,Whitespace."
        if not re.match(r"^[0-9]+$",str(attrs.get('price'))) or attrs.get('price')== 0:
            validation_error['price']=f"Enter a valid price."
        if not re.match(r"^[0-9]+$",str(attrs.get('stock'))) or attrs.get('stock')== 0:
            validation_error['stock']=f"Enter a valid stock."
        if len(validation_error)>0:
            raise serializers.ValidationError(validation_error)
        return attrs
    
    def product_save(self, shopid):
        shop = CustomUser.objects.get(id=shopid)
        try:
            shop_product_exist = ShopProducts.objects.get(
                Q(name=self.data.get('name'))&Q(price=self.data.get('price'))|
                Q(name=self.data.get('name'))&Q(discription=self.data.get('discription'))
            )
        except ShopProducts.DoesNotExist:
            return ShopProducts.objects.create(
                name = self.data.get('name'),price = self.data.get('price'),
                stock = self.data.get('stock'), discription = self.data.get('discription'),
                variation_id = self.data.get('variation'),categoryid_id = self.data.get('categoryid'),
                shop_id = shop.id
            )
        return False
        
    
    def image_save(self, image, productid):
        return ProductImages.objects.create(
            image = image,product_id = productid.id
        )
    

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ['image']



class ShopProductSerializer(serializers.ModelSerializer):
    '''
    
    '''
    class Meta:
        model = ShopProducts
        fields = [
            'id','name','price','stock',
            'categoryid','variation','discription'
        ]
