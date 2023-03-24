from superadmin.models import UserAddress,UsersDetails,ShopDetails
from rest_framework import serializers
import re


class SaveAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['address','pincode','city','state']

    def validate(self, attrs):
        validation_error = dict()
        if not re.match(r"^[a-zA-Z0-9\s]+$",attrs.get('address')):
            validation_error['address'] = "Only alphabets whitespaces and digits"
        if not len(str(attrs.get('pincode'))) == 6:
            validation_error['pincode'] = "pincode is not valid"
        if not re.match(r"^[a-zA-Z\s]+$",attrs.get('city')):
            validation_error['city'] = "city is not valid"
        if not re.match(r"^[a-zA-Z\s]+$",attrs.get('state')):
            validation_error['state'] = "state is not valid"
        if validation_error:
            raise serializers.ValidationError(validation_error)
        return True



    def save(self, shopid, userid):
        # user = UsersDetails.objects.get(id=userid)
        # shop = ShopDetails.objects.get(id=shopid)
        return UserAddress.objects.create(
            address = self.data.get('address'),
            pincode = self.data.get('pincode'),
            city = self.data.get('city'),
            state = self.data.get('state'),
            user_id = userid,
            shop_id = shopid
        )
