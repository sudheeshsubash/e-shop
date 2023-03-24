from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ChangePasswordSerializer,OtpSerializer
from superadmin.tokengeneratedecode import get_decoded_payload
from superadmin.custompermissions import CustomEndUserPermission
from superadmin.models import UsersDetails
from superadmin.otps import otp





class ChangePassword(APIView):

    permission_classes = [CustomEndUserPermission]

    def post(self, request, *args, **kwargs):
        payload = get_decoded_payload(request)
        user_details = UsersDetails.objects.get(id=payload['user_id'])
        change_password = ChangePasswordSerializer(user_details,data=request.data)
        if change_password.is_valid(raise_exception=True):
            otp_number = otp(user_details.phone_number)
            request.session['password'] = change_password.data.get("password")
            request.session['otp'] = otp_number()
            return Response({"result":"otp number sent to your phonenumber"})


class ChangeOtp(APIView):

    permission_classes = [CustomEndUserPermission]

    def get(self, request, *args, **kwargs):
        otp_serializer = OtpSerializer(request.data)
        if otp_serializer.is_valid(raise_exception=True):
            if int(otp_serializer.data.get('password')) == int(request.session['otp']):
                change_password = UsersDetails.objects.update(
                    password = request.session['password']
                )
                return Response({"result":f"{change_password.password}"})
            return Response({"error":"otp is not valid"})