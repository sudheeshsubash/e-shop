from rest_framework.response import Response
from admin_app1.tokens_permissions import CustomEndUserPermission
from rest_framework.views import APIView
from eshop_project import settings
from django.shortcuts import render
import razorpay
from django.views.decorators.csrf import csrf_exempt





class OrderCheckOut(APIView):
    '''
    
    '''
    
    @csrf_exempt
    def post(self, request):

        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        DATA = {
                "amount": 10000,
                "currency": "INR",
            }
        order = client.order.create(data=DATA)
        order_id = order['id']
        payment_id = request.POST.get('razorpay_payment_id')

        return Response({"orderid":f'{order_id}','paymentid':f'{payment_id}'})

    

    def get(self, request):
        return render(request, 'payment.html')

