from rest_framework import serializers
from superadmin.models import ShopCategorys,ShopDetails,ProductsCategorys,CustomUser,ShopStaff
import re
from django.contrib.auth.hashers import make_password


class ShopCategoryOrMagerCategorySerializer(serializers.ModelSerializer):
    '''
    this is the mager category , what kind of shop user is need 
    what type of shop category is available
    '''
    class Meta:
        model = ShopCategorys
        fields = ['shop_category_name','id']




class RegistrationShopDetailsSerializer(serializers.ModelSerializer):
    '''
    
    '''
    password2 = serializers.CharField(max_length=20)
    class Meta:
        model = ShopDetails
        fields = [
            'username','password','phone_number','place',
            'address','ownername','shop_category','email',
            'password2',
        ]
    
    def validate(self, attrs):
        
        username,password,phone_number,place, =  attrs.get('username'),attrs.get('password'),attrs.get('phone_number'),attrs.get('place')
        address,ownername,email,password2 = attrs.get('address'),attrs.get('ownername'),attrs.get('email'),attrs.get('password2')

        validationerror = dict() # this variable store all errors and finnaly raise all errors

        # validation start
        if not re.match(r"^[a-zA-Z\s0-9]+$",password):
            validationerror['password']={f"{password}":"Enter a valid password. This value may contain a-z,A-Z,0-9,Whitespace."}

        if not re.match(r"^[a-zA-Z\s0-9]+$",password2):
            validationerror['password2']={f"{password2}":"Enter a valid password. This value may contain a-z,A-Z,0-9,Whitespace."}
        
        if password != password2:
            raise serializers.ValidationError({"password":f'password , password2 is not same'})
        

        if not re.match(r"^[a-zA-Z0-9\s]+$",username):
            validationerror['username']={f"{username}":'Enter a valid username. This value may contain only letters'}

        if len(str(phone_number)) != 10:
            validationerror['phon_number'] = {f'{phone_number}':'Enter a valid phone_number. This value may contain 10 length.'}

        if not re.match(r"^[a-zA-Z\s]+$",place):
            validationerror['place'] = {f"{place}":'Enter a valid place. This value may contain only letters'}

        if re.match(r"^[a-zA-Z0-9\s]$",address):
            validationerror['address'] = {f"{address}":'Enter a valid address. This value may contain a-z,A-Z,09,whitespace.'}

        if not re.match(r"^[a-zA-Z\s]+$",ownername):
            validationerror['ownername'] = {f"{username}":'Enter a valid username. This value may contain only letters'}

        if not re.match("^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,3})$",email):
            validationerror['email'] = {f"{email}":'Enter a valid email.'}

        if len(validationerror) != 0:
            raise serializers.ValidationError(validationerror)
        return attrs
   


class ShopStaffSerializer(serializers.ModelSerializer):
    '''
    
    '''
    class Meta:
        model = ShopStaff
        fields = ['username','phone_number','email']

    def validate(self, attrs):
        validationerror = dict()
        if not re.match(r"^[a-zA-Z]{1}[a-zA-Z0-9\s]+$",attrs.get('username')):
            validationerror['username']={f"{attrs.get('username')}":'Enter a valid username. This value may contain only letters'}
        
        try:
            if not re.match("^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,3})$",attrs.get('email')):
                validationerror['email'] = {f"{attrs.get('email')}":'Enter a valid email.'}

            if len(str(attrs.get('phone_number'))) != 10:
                validationerror['phon_number'] = {f'{attrs.get("phone_number")}':'Enter a valid phone_number. This value may contain 10 length.'}
        except:
            pass
        
        if len(validationerror) != 0:
            raise serializers.ValidationError(validationerror)

        return attrs



class StaffRegistrationSerializer(serializers.ModelSerializer):
    '''

    '''
    password2 = serializers.CharField(max_length=20)
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username','password',
            'phone_number','password2'
        ]

    def validate(self, attrs):
        
        username,password = attrs.get('username'),attrs.get('password')
        phone_number,password2 = attrs.get('phone_number'),attrs.get('password2')

        validationerror = dict() # this variable store all errors and finnaly raise all errors

        # validation start
        if not re.match(r"^[a-zA-Z\s0-9]+$",password):
            validationerror['password']={f"{password}":"Enter a valid password. This value may contain a-z,A-Z,0-9,Whitespace."}

        if not re.match(r"^[a-zA-Z\s0-9]+$",password2):
            validationerror['password2']={f"{password2}":"Enter a valid password. This value may contain a-z,A-Z,0-9,Whitespace."}
        
        if password != password2:
            raise serializers.ValidationError({"password":f'password , password2 is not same'})
        

        if not re.match(r"^[a-zA-Z]{1}[a-zA-Z0-9\s]+$",username):
            validationerror['username']={f"{username}":'Enter a valid username. This value may contain only letters'}

        if len(str(phone_number)) != 10:
            validationerror['phon_number'] = {f'{phone_number}':'Enter a valid phone_number. This value may contain 10 length.'}

        if len(validationerror) != 0:
            raise serializers.ValidationError(validationerror)
        return attrs
   

    def save(self):
        return ShopStaff.objects.create(
            username = self.data.get('username'),
            password = make_password(self.data.get('password')),
            phone_number = self.data.get('phone_number'),
            role = 'shopstaff',
        )



class RegistrationShopDetailsOtpConfirmationSerializer(serializers.ModelSerializer):
    '''
    
    '''
    # password2 = serializers.CharField(max_length=20)
    class Meta:
        model = ShopDetails
        # exclude = 
        fields = ['id','username','ownername','phone_number','address','place']



class ProductCategorySerializer(serializers.ModelSerializer):
    '''
    
    '''
    class Meta:
        model = ProductsCategorys
        fields = '__all__'



class AddProductCategorySerializer(serializers.ModelSerializer):
    '''
    
    '''
    class Meta:
        model = ProductsCategorys
        fields = ['product_category_name']
    
    def validate(self, attrs):
        product_category_name = attrs.get('product_category_name')

        if not re.match(r"^[a-zA-Z\s]+$",product_category_name) or len(product_category_name)<4 or len(product_category_name) > 20:
            raise serializers.ValidationError({"error":'Enter a valid product_category_name. This value may contain only letters','length':"Four letter to twenty letter"})

        return attrs
    


class EditProductCategorySerializer(serializers.ModelSerializer):
    '''
    
    '''
    class Meta:
        model = ProductsCategorys
        fields = ['product_category_name']
    
    
    def validate(self, attrs):
        product_category_name = attrs.get('product_category_name')

        if not re.match(r"^[a-zA-Z\s]+$",product_category_name) or len(product_category_name)<4 or len(product_category_name) > 20:
            raise serializers.ValidationError({"error":'Enter a valid product_category_name. This value may contain only letters','length':"Four letter to twenty letter"})

        return attrs
    


class ShopStaffViewSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = ShopStaff
        fields = ['username','phone_number','email']