from rest_framework import serializers
from superadmin.models import CustomUser,EndUserCart,ShopProducts,EndUserWishlist,UsersDetails
import re



class RegistrationUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=20)
    class Meta:
        model = CustomUser
        fields = ['username','password','phone_number','email','confirm_password']

    def validate(self, attrs):

        validation_error = dict()

        if not re.match(r'^[a-zA-Z]{1}[a-zA-Z0-9/s]+$',attrs.get('password')):
            validation_error['password']='Enter a valid value for password'
            
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError({'password':'Confirm passwor is not match'})
        
        if not re.match(r"^[a-zA-Z]{1}[a-zA-Z0-9\s]+$",attrs.get('username')):
            validation_error['username']='Enter a valid value for username'

        if len(str(attrs.get('phone_number'))) != 10:
            validation_error['phon_number'] = 'Enter a valid phone_number. This value may contain 10 length.'

        # if not re.match("^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,3})$",attrs.get('email')):
        #     validation_error['email'] = 'Enter a valid email.'

        if validation_error:
            raise serializers.ValidationError(validation_error)
        
        return attrs


class RegistrationQuerysetToSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','email']


class OtpEnter(serializers.Serializer):
    otp = serializers.IntegerField()



class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersDetails
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


class UserCartSerializer(serializers.ModelSerializer):
    '''
    end user product add to cart database serializer
    '''
    class Meta:
        model=EndUserCart
        fields=['id','product','quantity','total_amount']


    def save(self, user_id, product_id, shop_id):
        '''
        custom save method parameters user id and produt id 
        the fetch price data and save to endusercart database
        '''
        try:
            products = ShopProducts.objects.get(id=product_id)
        except ShopProducts.DoesNotExist:
            print('product id is not valid')
            raise serializers.ValidationError({"error":"product is not valid"})
        
        try:
            checkproduct = EndUserCart.objects.get(user=user_id,product=product_id,shop=shop_id)
        except EndUserCart.DoesNotExist:
            print('product is not exist')

            return EndUserCart.objects.create(
                user_id = user_id,
                product_id = product_id,
                total_amount = products.price,
                shop_id = shop_id
            )
        checkproduct.quantity += 1
        checkproduct.total_amount = checkproduct.quantity*products.price
        checkproduct.save()
        return checkproduct
    
    

    @staticmethod
    def increse_quantity(cart_id):
        '''
        increse cart quantity, check product stock and cart quantity
        '''
        try:
            cart = EndUserCart.objects.get(id=cart_id)
        except EndUserCart.DoesNotExist:
            return 'error'
        else:
            try:
                produt = ShopProducts.objects.get(id=cart.product.id)
            except ShopProducts.DoesNotExist:
                print('product is not exist')
            
            if cart.quantity+1 >= produt.stock:
                return 0
        
            cart.quantity += 1
            cart.total_amount = cart.quantity*cart.product.price
            cart.save()
            return cart.quantity

    @staticmethod
    def decrese_quantity(cart_id):
        '''
        decrese cart quantity, check cart quantity is 0 
        then delete the cart queryset
        '''
        try:
            cart = EndUserCart.objects.get(id=cart_id)
        except EndUserCart.DoesNotExist:
            return 'error'
        if cart.quantity-1 == 0:
            cart.delete()
            return 0
        cart.quantity -= 1
        cart.total_amount = cart.quantity*cart.product.price
        cart.save()
        return cart.quantity


    @staticmethod
    def remove(cart_id):
        EndUserCart.objects.get(id=cart_id).delete()




class UserWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndUserWishlist
        fields = ['id','product']
    
    def save(self, user_id):
        return EndUserWishlist.objects.create(
            user_id = user_id,
            product_id = self.data.get('product')
        )


class UserAddProductToWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndUserWishlist
        fields = ['id','product']






class ViewProductSerializer(serializers.ModelSerializer):
    '''
    
    '''
    class Meta:
        model = ShopProducts
        fields = [
            'id','name','price','discription','stock',
            'is_available','categoryid','variation'
        ]
