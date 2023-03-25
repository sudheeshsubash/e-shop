from superadmin.models import UsersDetails,CustomUser
from rest_framework import serializers
import re



class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['password']


class OtpSerializer(serializers.Serializer):

    otp = serializers.IntegerField()

    def validate(self):
        if len(str(self.data.get('otp'))) != 4:
            raise serializers.ValidationError({"error":"otp is not valid"})