from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ChangePasswordSerializer,OtpSerializer
from superadmin.tokengeneratedecode import get_decoded_payload
from superadmin.custompermissions import CustomEndUserPermission
from superadmin.models import UsersDetails,CustomUser
from superadmin.otps import otp
from django.contrib.auth.hashers import make_password




class PasswordChangeOtp(APIView):

    permission_classes = [CustomEndUserPermission]

    def get(self, request, *args, **kwargs):
        payload = get_decoded_payload(request)
        user_details = UsersDetails.objects.get(id=payload['user_id'])
        otp_number = otp(user_details.phone_number)
        request.session['otp'] = otp_number()
        return Response({"result":f"{request.session['otp']}"})
    

    def post(self, request, *args, **kwargs):
        otp_serializer = OtpSerializer(request.data)
        print(otp_serializer.data)
        try:
            if int(otp_serializer.data.get('otp')) == request.session['otp']:
                request.session.flush()
                request.session['otpconfirm'] = True
                return Response({"result":"otp is valid, ready to change password"})
            return Response({"error":"Otp is not valid"})
        except Exception:
            return Response({"error":"Otp is not valid"})



class ChangePassword(APIView):

    permission_classes = [CustomEndUserPermission]

    def post(self, request, *args, **kwargs):
        try:
            if request.session['otpconfirm'] != True:
                return Response({"error":'try first otp validation api'})
        except Exception:
            return Response({"error":'try first otp validation api'})
        payload = get_decoded_payload(request)
        user_details = CustomUser.objects.get(id=payload['user_id'])
        change_password = ChangePasswordSerializer(request.data)
        user_details.password = make_password(change_password.data.get('password'))
        user_details.save()
        request.session.flush()
        return Response({"result":"password changed"})