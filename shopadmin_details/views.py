from django.shortcuts import render

# Create your views here.




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