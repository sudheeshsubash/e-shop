from rest_framework.views import APIView
from .serializers import OtpSerializer,ChangePasswordSerializer
from rest_framework.response import Response
from superadmin.tokengeneratedecode import get_decoded_payload
from superadmin.custompermissions import CustomAdminPermission
from superadmin.models import CustomUser
from superadmin.otps import otp
from django.contrib.auth.hashers import make_password
from rest_framework import status




class OtpGenerateAndCheck(APIView):

    permission_classes = [CustomAdminPermission]

    def get(self, request, *args, **kwargs):
        payload = get_decoded_payload(request)
        user = CustomUser.objects.get(id=payload['user_id'])
        otpnumber = otp(phone=user.phone_number)
        request.session['otpnumber'] = otpnumber()
        print(otpnumber())
        return Response({"result":f"Otp send to Phone"},status=status.HTTP_200_OK)
    

    def post(self, request, *args, **kwargs):
        otp_serializer = OtpSerializer(request.data)
        try:
            if int(otp_serializer.data.get('otp')) == request.session['otpnumber']:
                request.session.flush()
                request.session['otpconfirm'] = True
                return Response({"result":"otp is valid, ready to change password"},status=status.HTTP_100_CONTINUE)
            return Response({"error":"Otp is not valid"},status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error":"Generate first Otp"},status=status.HTTP_400_BAD_REQUEST)
        


class ChangePassword(APIView):

    permission_classes = [CustomAdminPermission]

    def post(self, request, *args, **kwargs):
        try:
            if request.session['otpconfirm'] != True:
                return Response({"error":'try first otp validation api'},status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"error":'try first otp validation api'},status=status.HTTP_400_BAD_REQUEST)
        payload = get_decoded_payload(request)
        user_details = CustomUser.objects.get(id=payload['user_id'])
        change_password = ChangePasswordSerializer(request.data)
        user_details.password = make_password(change_password.data.get('password'))
        user_details.save()
        request.session.flush()
        return Response({"result":"password changed"},status=status.HTTP_205_RESET_CONTENT)

