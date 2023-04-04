from rest_framework.response import Response
from rest_framework.views import APIView
from superadmin.custompermissions import CustomShopAdminPermission
from superadmin.models import ProductImages,ProductVariation,ProductsCategorys,ShopProducts
from django.db.models import Q
from superadmin.tokengeneratedecode import get_decoded_payload,check_jwt_user_id_kwargs_id
from .serializers import ProductCategorySerializer,ProductVariationSerializer,AddShopProductSerializer
from .serializers import ShopProductSerializer,ProductImageSerializer,ShopProductStockSerializer
from superadmin.paginations import CustomPageNumberPagination
from rest_framework import status


class ViewAllProductsBasedOnShopId(APIView):
    '''
    show all products
    '''
    permission_classes = [CustomShopAdminPermission]

    def get(self, request, *args, **kwargs):
        if not check_jwt_user_id_kwargs_id(request,kwargs['shopid']):
            return Response({'error':'You have no permission for access this shop methods'})
        pagination = CustomPageNumberPagination()
        try:
            shop_product_query = ShopProducts.objects.filter(shop=kwargs['shopid'])
        except ShopProducts.DoesNotExist:
            return Response({'result':'No products'})
        page = pagination.paginate_queryset(queryset=shop_product_query,request=request)
        shop_product_serializer = ShopProductSerializer(page,many=True)

        for product in shop_product_serializer.data:
            product_image_query = ProductImages.objects.filter(product=product['id'])
            product_image_serializer = ProductImageSerializer(product_image_query[0],many=False)

            product['image'] = product_image_serializer.data
        return pagination.get_paginated_response(shop_product_serializer.data)
    


class ShopProductsAdd(APIView):
    '''
    
    '''
    permission_classes = [CustomShopAdminPermission]

    def get(self, request, *args, **kwargs):
            
            if not check_jwt_user_id_kwargs_id(request,kwargs['shopid']):
                return Response({'error':"You don't have permission for access this shop method"})
            try:
                product_variation_query = ProductVariation.objects.all()
            except ProductVariation.DoesNotExist:
                return Response({'error':'NO Product Variations'})
            try:
                products_categorys_query = ProductsCategorys.objects.filter(Q(shop__isnull=True)|Q(shop=kwargs['shopid']))
            except ProductsCategorys.DoesNotExist:
                return Response({'error':'NO product categorys'})
            result = dict()
            product_variation_serializer = ProductVariationSerializer(product_variation_query,many=True)
            products_categorys_serializer = ProductCategorySerializer(products_categorys_query,many=True)
            result['variation'] = Response(product_variation_serializer.data).data
            result['category'] = Response(products_categorys_serializer.data).data
            return Response(result)
    

    def post(self, request, *args, **kwargs):
        if not check_jwt_user_id_kwargs_id(request,kwargs['shopid']):
            return Response({'error':"You don't have permission for access this shop method"})
        shop_product_serializer = AddShopProductSerializer(data=request.data)
        if shop_product_serializer.is_valid(raise_exception=True):
            shop_product_query = shop_product_serializer.product_save(kwargs['shopid'])
            if shop_product_query == False:
                return Response({'result':'Product is already exist'})
            product_image_serializer_list = list()

            for image in shop_product_serializer.validated_data['image']:
                product_image_save_query = shop_product_serializer.image_save(image=image,productid=shop_product_query)
                product_image_serializer_list.append(product_image_save_query)

            product_image_serializer = ProductImageSerializer(product_image_serializer_list,many=True)
            shop_product_result = Response(shop_product_serializer.data).data
            shop_product_result['image'] = Response(product_image_serializer.data).data
            return Response({"result":shop_product_result})



class ShopProductsEdit(APIView):
    '''
    
    '''
    permission_classes = [CustomShopAdminPermission]

    def get(self, request, *args, **kwargs):
        
        if not check_jwt_user_id_kwargs_id(request, kwargs['shopid']):
            return Response({'error':"You don't have permission for access this shop methods"})
        
        shop_product_query = ShopProducts.objects.filter(id=kwargs['productid'])
        
        if not shop_product_query:
            return Response({'result':'No products'})

        shop_product_serializer = ShopProductSerializer(shop_product_query,many=True)

        for product in shop_product_serializer.data:
            product_image_query = ProductImages.objects.filter(product=product['id'])
            product_image_serializer = ProductImageSerializer(product_image_query,many=True)
            product['image'] = Response(product_image_serializer.data).data
        return Response(shop_product_serializer.data)
    

    def patch(self, request, *args, **kwargs):

        if not check_jwt_user_id_kwargs_id(request, kwargs['shopid']):
            return Response({'error':"You don't have permission for access this shop methods"})
        try:
            shop_product_query = ShopProducts.objects.get(id=kwargs['productid'])
        except ShopProducts.DoesNotExist:
            return Response({"error":"No product"})
        if not shop_product_query:
            return Response({'result':'No products'})

        shop_product_serializer = ShopProductSerializer(shop_product_query,data=request.data)
        if shop_product_serializer.is_valid(raise_exception=True):
            shop_product_serializer.save()
            return Response({'result':shop_product_serializer.data},status=status.HTTP_200_OK)


    def delete(self, request, *args, **kwargs):
        if not check_jwt_user_id_kwargs_id(request, kwargs['shopid']):
            return Response({'error':"You don't have permission for access this shop methods"})
        try:
            ShopProducts.objects.get(id=kwargs['productid']).delete()
        except ShopProducts.DoesNotExist:
            return Response({"error":"Invalid productid"},status=status.HTTP_404_NOT_FOUND)
        return Response({"result":"Product deleted"},status=status.HTTP_200_OK)



class ShopProductImageEdit(APIView):
    '''
    
    '''
    permission_classes = [CustomShopAdminPermission]
        
    def patch(self, request, *args, **kwargs):
        if not check_jwt_user_id_kwargs_id(request,kwargs['shopid']):
            return Response({'error':"You don't have permission for access this shop methods"})
        
        try:
            shop_product_image = ProductImages.objects.get(id=kwargs['imageid'])
        except ProductImages.DoesNotExist:
            return Response({'error':'No image is exist'})
        
        product_image_serializer = ProductImageSerializer(shop_product_image,data=request.data)
        if product_image_serializer.is_valid(raise_exception=True):
            product_image_serializer.save()
            return Response({'result':f"product image update successfully {product_image_serializer.data}"})



class AddProductImage(APIView):

    permission_classes = [CustomShopAdminPermission]

    def post(self, request, *args, **kwargs):
        product_image_serializer = ProductImageSerializer(data=request.data)
        if product_image_serializer.is_valid(raise_exception=True):
            product_image_serializer.save()
            return Response({"result":"add new image for products"},status=status.HTTP_200_OK)



class ViewAllProductStock(APIView):

    permission_classes = [CustomShopAdminPermission]

    def get(self, request, *args, **kwargs):
        product_stock_query = ShopProducts.objects.filter(shop=kwargs['shopid']).values('stock','name')
        pagination = CustomPageNumberPagination()
        page = pagination.paginate_queryset(queryset=product_stock_query,request=request)
        product_stock_serializer = ShopProductStockSerializer(page,many=True)
        return pagination.get_paginated_response(product_stock_serializer.data)
    

class AddProductStock(APIView):

    permission_classes = [CustomShopAdminPermission]

    def patch(self, request, *args, **kwargs):
        try:
            product_stock_query = ShopProducts.objects.get(shop=kwargs['shopid'],id=kwargs['productid'])
        except ShopProducts.DoesNotExist:
            return Response({"error":"shopid is not valid"},status=status.HTTP_404_NOT_FOUND)
        
        product_stock_serializer = ShopProductStockSerializer(product_stock_query,data=request.data)
        if product_stock_serializer.is_valid(raise_exception=True):
            product_stock_serializer.save()
            return Response({"result":"product stock is updated"},status=status.HTTP_200_OK)