from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from superadmin.models import EndUserCart,EndUserOrders,OrderProducts,UserAddress
from django.views.decorators.csrf import csrf_exempt
from superadmin.custompermissions import CustomEndUserPermission
import razorpay
from eshop_project import settings
from .serializers import SaveAddressSerializer,ChoosePaymentAddressSerializer,AllOrderViewListSerializer,OrderProductsSerializer
from superadmin.tokengeneratedecode import query_param_token_decode,check_online_place_order,get_decoded_payload
from rest_framework import status
from superadmin.paginations import CustomPageNumberPagination



class PlaceOrderToSave:

    def total_amout(self, user_id):
        amount = int()
        for cartitem in EndUserCart.objects.filter(user=user_id):
            amount += cartitem.total_amount
        return amount

    def online_payment(self, user_id, shop_id, payment_type, address, orderid=None, paymentid=None):
        cart = EndUserCart.objects.filter(user=user_id)
        if not cart:
            return Response({'result':'No cart Product'})
        print(address)
        address_query = UserAddress.objects.get(id=address)
        enduserorder = EndUserOrders.objects.create(
            shop_id = shop_id,
            user_id = user_id,
            payment_id = paymentid,
            order_id = orderid,
            total_amount = self.total_amout(user_id=user_id),
            order_status = 'complete',
            payment_type = payment_type,
            payment_credit = self.total_amout(user_id=user_id),
            address_id = address_query.id
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

    def cash_on_payment(self, user_id, shop_id, payment_type, address,orderid=None, paymentid=None):
        cart = EndUserCart.objects.filter(user=user_id)
        if not cart:
            return 0
        address_query = UserAddress.objects.get(id=address)
        print(address_query)
        enduserorder = EndUserOrders.objects.create(
            shop_id = shop_id,
            user_id = user_id,
            total_amount = self.total_amout(user_id=user_id),
            order_status = 'pending',
            payment_type = payment_type,
            address_id = address_query.id
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



class ChooseAddressAndPaymentType(APIView):
    '''
    choose payment type and address
    '''
    permission_classes = [CustomEndUserPermission]

    def get(self, request, *args, **kwargs):
        return Response({"result":{"payment_type":"required field","address":'required field'}})


    def post(self, request, *args, **kwargs):
        choose_address_payment_type = ChoosePaymentAddressSerializer(data=request.data)
        if choose_address_payment_type.is_valid(raise_exception=True):
            request.session['choose'] = True
            request.session['address'] = choose_address_payment_type.data.get("address")
            request.session['paymenttype'] = choose_address_payment_type.data.get("payment_type")
        return Response({"result":"Payment_type and address Choosed"})



class AddUserAddress(APIView):
    '''
    User Address 
    '''
    permission_classes = [CustomEndUserPermission]

    def post(self, request, *args, **kwargs):
        payload = get_decoded_payload(request)
        address_serializer = SaveAddressSerializer(data=request.data)
        if address_serializer.is_valid(raise_exception=True):
            address = address_serializer.save(shopid=kwargs['shopid'],userid=payload['user_id'])
            print(address,address_serializer.data)
            return Response({"result":address_serializer.data},status=status.HTTP_200_OK)



class PlaceOrderOnlinePurchase(APIView):

    def get(self, request, *args, **kwargs):
        # try:
        #     request.session['choose']
        # except Exception:
        #     return Response({"error":"first choose which method and address"})
        # print(request.session['paymenttype'])
        # if request.session['paymenttype'] == 'online':
            jwt = request.query_params.get('jwt')
            if jwt is None:
                return Response({'userid ':'please pass jwt token (?jwt=value)'})
            if check_online_place_order(jwt,kwargs):
                return Response({"error":"You don't have permission for access this shop method"})
            userid =query_param_token_decode(jwt)
            findamount = PlaceOrderToSave()
            amount = findamount.total_amout(user_id=userid['user_id'])
            if not amount:
                return Response({"error":"No Cart Product,"})
            client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
            DATA = {
                    "amount": amount*100,
                    "currency": "INR",
                    "receipt": "order_rcptid_11",
                }
            order = client.order.create(data=DATA)
            request.session['orderid'] = order['id']
            print(request.session['orderid'])
            return render(request,'payment.html',context=order,status=status.HTTP_200_OK)
        # else:
        #     return Response({"error":"This is Online method but you choose cash on purchase"})


    def post(self, request, *args, **kwargs):
        # try:
        #     request.session['choose']
        # except Exception:
        #     return Response({"error":"first choose which method and address"})
        # if request.session['paymenttype'] == 'online':
            data = request.POST.dict()
            payment_id = data.get('razorpay_payment_id')
            jwt = request.query_params.get('jwt')
            userid =query_param_token_decode(jwt)
            if payment_id:
                client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
                place_order = PlaceOrderToSave()
                amount = place_order.total_amout(user_id=userid['user_id']) * 100
                payment = client.payment.capture(payment_id, amount=amount)
                if payment['status'] == 'captured':
                    order = place_order.online_payment(
                        user_id=int(userid['user_id']),
                        payment_type='online',
                        orderid=request.session.get('orderid'),
                        paymentid=payment_id,
                        shop_id=kwargs['shopid'],
                        address = 1
                    )
                    request.session.flush()
                    return Response({"result":"Order is Place"},status=status.HTTP_200_OK)
                elif payment['status'] == 'failed':
                    return Response({"error":"Payment Transation is Failed"},status=status.HTTP_400_BAD_REQUEST)
                elif payment['status'] == 'authorized':
                    return Response({"error":"Payment Transation is Authorized"},status=status.HTTP_400_BAD_REQUEST)

        # else:
        #     return Response({"erro"})
        
    
class PlaceOrderCashOnPurchase(APIView):

    permission_classes = [CustomEndUserPermission]

    def post(self, request, *args, **kwargs):
        try:
            request.session['choose']
        except Exception:
            return Response({"error":"first choose which method and address"})
        if request.session['paymenttype'] == 'cashondelivery':
            payload = get_decoded_payload(request)
            cash_on_place = PlaceOrderToSave()
            orderplace_check = cash_on_place.cash_on_payment(
                user_id=payload['user_id'],
                payment_type=request.session['paymenttype'],
                shop_id=kwargs['shopid'],
                address=request.session['address']
            )
            request.session.flush()
            if orderplace_check:
                return Response({"result":"Order Placed"})
            return Response({"error":"NO cart products"})
        
        else:
            return Response({"error":"selected method is online"})


class ViewAllOrders(APIView):
    
    permission_classes = [CustomEndUserPermission]

    def get(self, request, *args, **kwargs):
        payment_status = request.query_params.get('status')
        pagination = CustomPageNumberPagination()
        if payment_status is None:
            orders_list = EndUserOrders.objects.filter(shop=kwargs['shopid']).order_by('-create')
        elif payment_status == 'cancle':
            orders_list = EndUserOrders.objects.filter(shop=kwargs['shopid'],order_status='cancle').order_by('-create')
        elif payment_status == 'refund':
            orders_list = EndUserOrders.objects.filter(shop=kwargs['shopid'],order_status='refund').order_by('-create')
        else:
            return Response({"error":"query param error"})
        if not orders_list:
            return Response({"error":"No Orders"})
        return_orders_list = list()
        page = pagination.paginate_queryset(orders_list,request)
        order_view_serializer = AllOrderViewListSerializer(page,many=True)
        for order in order_view_serializer.data:
            order_products = OrderProducts.objects.get(order = order['id'])
            order_products_serializer = OrderProductsSerializer(order_products,many=False)
            order['product'] = order_products_serializer.data
        return pagination.get_paginated_response(order_view_serializer.data)



