from superadmin.models import UsersDetails
from rest_framework import serializers




class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersDetails
        fields = ['password']


class OtpSerializer(serializers.Serializer):
    otp = serializers.IntegerField()