from rest_framework.response import Response
from rest_framework.views import APIView
from superadmin.custompermissions import CustomShopAdminPermission
from superadmin.models import ProductImages,ProductVariation,ProductsCategorys,ShopProducts
from django.db.models import Q
from superadmin.tokengeneratedecode import get_decoded_payload
from .serializers import ProductCategorySerializer,ProductVariationSerializer,AddShopProductSerializer
from .serializers import ShopProductSerializer,ProductImageSerializer
from superadmin.paginations import CustomPageNumberPagination





class ViewAllProductsBasedOnShopId(APIView):
    '''
    show all products
    '''
    permission_classes = [CustomShopAdminPermission]

    def get(self, request):
        pagination = CustomPageNumberPagination()
        userid_form_token = get_decoded_payload(request)
        try:
            shop_product_query = ShopProducts.objects.filter(shop=userid_form_token['user_id'])
        except ShopProducts.DoesNotExist:
            return Response({'result':'No products'})
        page = pagination.paginate_queryset(queryset=shop_product_query,request=request)
        shop_product_serializer = ShopProductSerializer(page,many=True)

        for product in shop_product_serializer.data:
            product_image_query = ProductImages.objects.filter(product=product['id'])
            product_image_serializer = ProductImageSerializer(product_image_query,many=True)

            product['image'] = product_image_serializer.data
        return pagination.get_paginated_response(shop_product_serializer.data)



class ShopProductsAddEditDelete(APIView):
    '''
    Addproduct, Editproduct, Deleteproduct
    '''
    permission_classes = [CustomShopAdminPermission]

    def get(self, request):
        query_param_type = request.query_params.get('type')
        userid_form_token = get_decoded_payload(request)

        if query_param_type is None:
            return Response({'result':'query param need (?type=add/edit)'})
        
        if query_param_type == 'add':
            try:
                product_variation_query = ProductVariation.objects.all()
            except ProductVariation.DoesNotExist:
                return Response({'error':'NO Product Variations'})
            try:
                products_categorys_query = ProductsCategorys.objects.filter(Q(shop__isnull=True)|Q(shop=userid_form_token['user_id']))
            except ProductsCategorys.DoesNotExist:
                return Response({'error':'NO product categorys'})
            result = dict()
            product_variation_serializer = ProductVariationSerializer(product_variation_query,many=True)
            products_categorys_serializer = ProductCategorySerializer(products_categorys_query,many=True)
            result['variation'] = Response(product_variation_serializer.data).data
            result['category'] = Response(products_categorys_serializer.data).data
            return Response(result)


        if query_param_type != 'edit':
            return Response({'result':'only ?type=add/edit is valid'})

        product_id = request.query_params.get('productid')
        if product_id is None:
            return Response({'result':'query param need (productid)'})
        try:
            shop_product_query = ShopProducts.objects.filter(id=product_id)
        except ShopProducts.DoesNotExist:
            return Response({'result':'No products'})
        shop_product_serializer = ShopProductSerializer(shop_product_query,many=True)

        for product in shop_product_serializer.data:
            product_image_query = ProductImages.objects.filter(product=product['id'])
            product_image_serializer = ProductImageSerializer(product_image_query,many=True)
            product['image'] = Response(product_image_serializer.data).data
        return Response(shop_product_serializer.data)



    def post(self, request):
        query_param_type = request.query_params.get('type')
        userid_form_token = get_decoded_payload(request)

        if query_param_type != 'add':
            return Response({'result':'query param need (?type=add)'})
        
        shop_product_serializer = AddShopProductSerializer(data=request.data)
        if shop_product_serializer.is_valid(raise_exception=True):
            shop_product_query = shop_product_serializer.product_save(userid_form_token['user_id'])
            if shop_product_query == False:
                return Response({'result':'Product is already exist'})
            product_image_serializer_list = list()

            for image in shop_product_serializer.validated_data['image']:
                product_image_save_query = shop_product_serializer.image_save(image=image,productid=shop_product_query)
                product_image_serializer_list.append(product_image_save_query)

            product_image_serializer = ProductImageSerializer(product_image_serializer_list,many=True)
            shop_product_result = Response(shop_product_serializer.data).data
            shop_product_result['image'] = Response(product_image_serializer.data).data
            return Response(shop_product_result)



    def patch(self, request):
        query_param_type = request.query_params.get('type')
        product_id = request.query_params.get('productid')
        userid_form_token = get_decoded_payload(request)

        if query_param_type is None or product_id is None:
            return Response({'result':'query param need (?type=edit) or (productid)'})
        if query_param_type != 'edit':
            return Response({'result':'only ?type=edit is valid'})
        
        
        return Response({'result':'patch method'})
