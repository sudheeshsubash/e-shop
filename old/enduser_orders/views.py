from rest_framework.response import Response
from admin_app1.tokens_permissions import CustomEndUserPermission
from rest_framework.views import APIView
from eshop_project import settings
from django.shortcuts import render
import razorpay
from django.views.decorators.csrf import csrf_exempt
from admin_app1.tokens_permissions import get_decoded_payload
from enduser_product.models import EndUserCart
from .models import EndUserOrders,OrderProducts
from enduser_orders.serializers import ViewEndUserOrdersSerializer
from datetime import datetime




class OrderCheckOutOnlinePurchase(APIView):
    '''
    
    '''
    # permission_classes=[CustomEndUserPermission]
    
    @csrf_exempt
    def post(self, request):
        userid = request.query_params.get('uid')
        placeorder = PlaceOrderOrSaveCartDataToOrderTable()
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        DATA = {
                "amount": 100,
                "currency": "INR",
            }
        order = client.order.create(data=DATA)
        order_id = order['id']
        payment_id = request.POST.get('razorpay_payment_id')


        order = placeorder.cart_to_order_place(user_id=int(userid),payment_type='onlinepurchase',orderid=order_id,paymentid=payment_id)
        return Response({'msg':f'order is done {order.id}, {order.create}'})



    def get(self, request):
        userid = request.query_params.get('userid')
        if userid is None:
            return Response({'userid ':'please pass userid query params (userid)'})
        findamount = PlaceOrderOrSaveCartDataToOrderTable()
        amount = findamount.total_amout_of_cart(user_id=userid)
        context = {
            'amount' : amount*100
        }
        return render(request, 'payment.html',context=context)



class OrderCheckOutCashOnPurchase(APIView):
    '''
    
    '''
    permission_classes=[CustomEndUserPermission]

    def post(self, request):
        decoded_payload = get_decoded_payload(request)
        placeorder = PlaceOrderOrSaveCartDataToOrderTable()
        order = placeorder.cart_to_order_place(user_id=decoded_payload['user_id'],payment_type='cashonpurchase')
        if type(order) is str:
            return Response({'msg':f'{order}'})
        return Response({'msg':f'order is done {order.id}, {order.create}'})



class PlaceOrderOrSaveCartDataToOrderTable:
    '''
    
    '''


    def total_amout_of_cart(self, user_id):
        amount = int()
        try:
            for cartitem in EndUserCart.objects.filter(user=user_id):
                amount += cartitem.price
            return amount
        
        except:
            return 100
    
    
    def cart_to_order_place(self, user_id, payment_type, orderid=None, paymentid=None):
        try:
            cart = EndUserCart.objects.filter(user=user_id)
        except EndUserCart.DoesNotExist:
            print('cart have no element')
            
        if len(cart) == 0:
            return 'cart have no data or product'
        enduserorder = EndUserOrders.objects.create(
            shop_id = cart[0].product.shop_id.id,
            user_id = user_id,
            payment_id = paymentid,
            order_id = orderid,
            amount = self.total_amout_of_cart(user_id=user_id),
            status = 'pending',
            payment_type = payment_type
        )

        for cart_item in cart:
            OrderProducts.objects.create(
                order_id = enduserorder.id,
                product_id = cart_item.product.id,
                product_name = cart_item.product.name,
                product_price = cart_item.product.price,
                total = cart_item.price,
                quantity = cart_item.quantity
            )
        
        cart.delete()
        
        return enduserorder
    


class ViewMyOrder(APIView):
    '''
    
    '''
    permission_classes=[CustomEndUserPermission]
    def get(self, request):
        decodeuserid = get_decoded_payload(request=request)
        try:
            orderdetails = EndUserOrders.objects.filter(user=decodeuserid['user_id'])
        except EndUserOrders.DoesNotExist:
            return Response({'error':f'user have no orders'})
        return Response({'orders':f'{orderdetails}'})
    

    def patch(self, request):
        '''
        refund and puchase cancle method
        '''
        orderid = request.query_params.get('orderid')
        if orderid is None:
            return Response({'orderid':'query params orderid is must needed'})
        try:
            orderdetails = EndUserOrders.objects.get(id=orderid)
        except EndUserOrders.DoesNotExist:
            return Response(f"{orderid} is not valid")

        date_of_order = datetime.strptime(str(orderdetails.create),"%Y-%m-%d %H:%M:%S.%f%z")
        today_date =datetime.strptime(str(datetime.now()),"%Y-%m-%d %H:%M:%S.%f")

        if date_of_order.year == today_date.year and date_of_order.month == today_date.month and date_of_order.day == today_date.day:

            if orderdetails.payment_type == 'onlinepurchase':

                client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
                amount = orderdetails.amount * 100

                try:
                    client.payment.capture(orderdetails.payment_id, int(amount))
                    refund = client.payment.refund(orderdetails.payment_id, {"amount": amount})
                except:
                    return Response(' refund failed')

                else:
                    if not orderdetails.status == 'cancle':
                        orderdetails.status = 'cancel'
                        orderdetails.save()
                        if orderdetails.staff:
                            EndUserOrders.objects.create(
                                shop_id = orderdetails.shop.id,
                                user_id = orderdetails.user.id,
                                refund_order_id = orderdetails.id,
                                staff_id = orderdetails.staff.id,
                                payment_id = orderdetails.payment_id,
                                order_id = orderdetails.order_id,
                                amount = orderdetails.amount,
                                status = 'refund',
                                payment_type = 'onlinepurchase'
                            )
                        EndUserOrders.objects.create(
                                shop_id = orderdetails.shop.id,
                                user_id = orderdetails.user.id,
                                refund_order_id = orderdetails.id,
                                payment_id = orderdetails.payment_id,
                                order_id = orderdetails.order_id,
                                amount = orderdetails.amount,
                                status = 'refund',
                                payment_type = 'onlinepurchase'
                            )
                        return Response({"msg":f"{orderdetails} is canceld"})
                    return Response(f"{orderdetails} is already canceld")

            if not orderdetails.status == 'cancle':
                orderdetails.status = 'cancle'
                orderdetails.save()
                return Response({"msg":f"{orderdetails} this order is canceld"})
            return Response({'msg':f"{orderdetails} is olready canceld"})
        
        
        return Response(f"you can't possible of cancle this order:- {orderdetails}")




class ViewMyOrderProducts(APIView):
    '''
    view order all products
    '''
    permission_classes=[CustomEndUserPermission]
    def get(self, request):
        orderid = request.query_params.get('orderid')
        if orderid is None:
            return Response({"orderid":'query param orderid is needed'})
        try:
            orderproducts = OrderProducts.objects.filter(order=orderid)
        except OrderProducts.DoesNotExist:
            return Response({'error':f'{orderid} is not valid'})
        
        return Response({'msg':f'{orderproducts}'})



