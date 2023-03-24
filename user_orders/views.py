from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from superadmin.models import EndUserCart,EndUserOrders,OrderProducts
from django.views.decorators.csrf import csrf_exempt
from superadmin.custompermissions import CustomEndUserPermission
import razorpay
from eshop_project import settings
from .serializers import SaveAddressSerializer
from superadmin.tokengeneratedecode import query_param_token_decode,check_online_place_order,get_decoded_payload



class OnlinePlaceORder(APIView):
    def get(self, request, *args, **kwargs):
        jwt = request.query_params.get('jwt')
        if jwt is None:
            return Response({'userid ':'please pass jwt token (?jwt=value)'})
        if check_online_place_order(jwt,kwargs):
            return Response({"error":"You don't have permission for access this shop method"})
        userid =query_param_token_decode(jwt)
        findamount = PlaceOrderOrSaveCartDataToOrderTable()
        amount = findamount.total_amout_of_cart(user_id=userid['user_id'])
        print(amount)
        context = {'amount' : amount*100}
        return render(request,'payment.html',context=context)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        jwt = request.query_params.get('jwt')
        if jwt is None:
            return Response({'userid ':'please pass jwt token (?token=value)'})
        userid =query_param_token_decode(jwt)
        placeorder = PlaceOrderOrSaveCartDataToOrderTable()
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        DATA = {
                "amount": 100,
                "currency": "INR",
            }
        order = client.order.create(data=DATA)
        order_id = order['id']
        payment_id = request.POST.get('razorpay_payment_id')

        order = placeorder.cart_to_order_place(user_id=int(userid['user_id']),payment_type='online',orderid=order_id,paymentid=payment_id)
        return Response({'msg':f'order is done '})



class PlaceOrderOrSaveCartDataToOrderTable:

    def total_amout_of_cart(self, user_id):
        amount = int()
        for cartitem in EndUserCart.objects.filter(user=user_id):
            amount += cartitem.total_amount
        return amount

    def cart_to_order_place(self, user_id, shop_id, payment_type, orderid=None, paymentid=None):
        cart = EndUserCart.objects.filter(user=user_id)
        if not cart:
            return Response({'result':'No cart Product'})
        enduserorder = EndUserOrders.objects.create(
            shop_id = shop_id,
            user_id = user_id,
            payment_id = paymentid,
            order_id = orderid,
            total_amount = self.total_amout_of_cart(user_id=user_id),
            order_status = 'complete',
            payment_type = payment_type,
            payment_credit = self.total_amout_of_cart(user_id=user_id)
        )
        for cart_item in cart:
            OrderProducts.objects.create(
                order_id = enduserorder.id,
                shop_id = cart_item.product.shop.id,
                product_id = cart_item.product.id,
                product_name = cart_item.product.name,
                product_price = cart_item.product.price,
                quantity = cart_item.quantity,
                total = cart_item.total_amount,
                discription = cart_item.product.discription
            )
        cart.delete()
        return enduserorder



class AddUserAddress(APIView):
    '''
    
    '''
    permission_classes = [CustomEndUserPermission]
    def post(self, request, *args, **kwargs):
        payload = get_decoded_payload(request)
        address_serializer = SaveAddressSerializer(data=request.data,many=True)
        if address_serializer.is_valid(raise_exception=True):
            address = address_serializer.save(shopid=kwargs['shopid'],userid=payload['user_id'])
            print(address,address_serializer.data)
            return Response({"result":address_serializer.data})
    