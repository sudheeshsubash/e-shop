from rest_framework.views import APIView
from .serializers import OtpSerializer,ChangePasswordSerializer
from rest_framework.response import Response
from superadmin.tokengeneratedecode import get_decoded_payload
from superadmin.custompermissions import CustomAdminPermission
from superadmin.models import CustomUser
from superadmin.otps import otp
from django.contrib.auth.hashers import make_password





class OtpGenerateAndCheck(APIView):

    permission_classes = [CustomAdminPermission]

    def get(self, request, *args, **kwargs):
        payload = get_decoded_payload(request)
        user = CustomUser.objects.get(id=payload['user_id'])
        otpnumber = otp(phone=user.phone_number)
        request.session['otpnumber'] = otpnumber()
        return Response({"result":f"{request.session['otpnumber']}"})
    
    def post(self, request, *args, **kwargs):
        otp_serializer = OtpSerializer(request.data)
        try:
            if int(otp_serializer.data.get('otp')) == request.session['otpnumber']:
                request.session.flush()
                request.session['otpconfirm'] = True
                return Response({"result":"otp is valid, ready to change password"})
            return Response({"error":"Otp is not valid"})
        except Exception:
            return Response({"error":"Generate first Otp"})