from .serializers import StaffViewOrdersSerializer,OrderProductsSerializer,ChangeStatusSerializer
from rest_framework.views import APIView
from superadmin.custompermissions import CustomShopStaffPermission
from superadmin.models import EndUserOrders,OrderProducts
from rest_framework.response import Response
from datetime import datetime
from django_filters import rest_framework as filters
from superadmin.tokengeneratedecode import get_decoded_payload,get_tokens_for_user
from .serializers import LoginSerializer
from django.contrib.auth import authenticate
from superadmin.models import ShopStaff


class LoginStaff(APIView):

    def get(self, request, *args, **kwargs):
        login_serializer = LoginSerializer(request.data) 
        if login_serializer.validate():
            username = login_serializer.data.get('username')
            password = login_serializer.data.get('password')
            users = authenticate(username=username,password=password)
            if users is not None:
                try:
                    user_details = ShopStaff.objects.get(customuser_ptr_id=users.id)
                except Exception as e:
                    return Response(e)
                if int(user_details.shop.id) == kwargs['shopid']:
                    token = get_tokens_for_user(user=users)

                    return Response({'token':token})
            return Response({'error':f'{username} and {password} is not correct'})

 

class StaffOrderView(APIView):

    # permission_classes = [CustomShopStaffPermission]

    def get(self, request, *args, **kwargs):
        date = request.query_params.get('date')
        if date is not None:
            orders_list = EndUserOrders.objects.filter(
            shop=kwargs['shopid'],create__date=date
            )
        else:
            today_date = datetime.strptime(str(datetime.now()),"%Y-%m-%d %H:%M:%S.%f")
            orders_list = EndUserOrders.objects.filter(
                shop=kwargs['shopid'],create__date=today_date
            )
        if not orders_list:
            return Response({"error":"Shop Have No Orders"})
        return_orders_list = list()
        order_view_serializer = StaffViewOrdersSerializer(orders_list,many=True)
        for order in order_view_serializer.data:
            order_products = OrderProducts.objects.get(order = order['id'])
            order_products_serializer = OrderProductsSerializer(order_products,many=False)
            order['product'] = order_products_serializer.data
        return Response({"result":order_view_serializer.data})



class ViewAllOrders(APIView):

    def get(self, request, *args, **kwargs):

        orders_list = EndUserOrders.objects.filter(shop=kwargs['shopid'])

        if not orders_list:
            return Response({"error":"Shop Have No Orders"})
        return_orders_list = list()
        order_view_serializer = StaffViewOrdersSerializer(orders_list,many=True)
        for order in order_view_serializer.data:
            order_products = OrderProducts.objects.get(order = order['id'])
            order_products_serializer = OrderProductsSerializer(order_products,many=False)
            order['product'] = order_products_serializer.data
        return Response({"result":order_view_serializer.data})



class ViewOrderDetails(APIView):
    
    def get(self, request, *args, **kwargs):
        
        order_product = OrderProducts.objects.filter(order=kwargs['orderid'])
        if not order_product:
            return Response({"error":"Orderid is not valid"})
        order_product_serializer = OrderProductsSerializer(order_product,many=True)
        order_details = EndUserOrders.objects.get(id=order_product[0].id)
        order_details_serializer = StaffViewOrdersSerializer(order_details)
        order_product_serializer.data[0]['order'] = order_details_serializer.data
        return Response(order_product_serializer.data)
    


class ConfirmOrderOrChangeStatus(APIView):

    permission_classes = [CustomShopStaffPermission]

    def get(self, request, *args, **kwargs):
        payment_type_list = ['pending','cancel','complete','refund']
        return Response({"result":payment_type_list})

    def patch(self, request, *args, **kwargs):
        payload = get_decoded_payload(request)
        try:
            order_product = EndUserOrders.objects.get(order=kwargs['orderid'])
            if order_product.payment_type == 'online':
                raise Exception
        except Exception:
            return Response({"error":"orderid is not valid"})
        payment_change_serializer = ChangeStatusSerializer(request.data)
        order_product.staff = payload['user_id']
        order_product.payment_credit = payment_change_serializer.data.get('payment')
        return Response({"result":"Payment Details Updated"})




class RefundPaymentStatus(APIView):
    permission_classes = [CustomShopStaffPermission]