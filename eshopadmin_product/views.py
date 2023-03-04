from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from admin_app1.tokens_permissions import CustomShopAdminPermission,get_decoded_payload
from .serializers import ShopCategorySerializers,ShopCategorys,ShopProductSerializers,UpdateShopProductDetails,AddProductImagesSerializer
from rest_framework import status
from .models import ShopProducts,ShopCategorys
from admin_app1.paginations import CustomPageNumberPagination
from rest_framework.views import APIView




class AddToCategoryViewEdit(APIView):
    '''
    add to category
    view category
    edit category
    '''
    permission_classes=[CustomShopAdminPermission]

    def post(self, request):
        serializer = ShopCategorySerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg':serializer.data},status=status.HTTP_201_CREATED)
        return Response({'msg':'data not valid'},status=status.HTTP_406_NOT_ACCEPTABLE)
    


    def get(self, request):
        category = ShopCategorys.objects.all()
        serializer = ShopCategorySerializers(category,many=True)
        return Response(serializer.data)
        


    def patch(self, request):
        category_id = request.query_params.get('cid')
        try:
            category = ShopCategorys.objects.get(id=category_id)
        except ShopCategorys.DoesNotExist:
            return Response({'msg':f'{category_id} is not valid'})
        
        serializer = ShopCategorySerializers(category,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg':serializer.data})
        return Response({'msg':'data is not valid'})





class AddProductViewProductsEditProductDeleteProduct(APIView):
    '''
    Add product 
    view all products
    edit product
    delete product
    '''
    permission_classes=[CustomShopAdminPermission]

    def post(self, request):
        serializer = ShopProductSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            decoded_token = get_decoded_payload(request)
            product = serializer.save(decoded_token['user_id'])
            return Response({'msg':f'{product} created'},status=status.HTTP_201_CREATED)
        return Response({'msg':'not done'},status=status.HTTP_404_NOT_FOUND)
    


    def get(self, request):
        pagination = CustomPageNumberPagination()
        pagination_serializer = ShopProductSerializers(pagination.paginate_queryset(ShopProducts.objects.all(),request),many=True)
        return pagination.get_paginated_response(pagination_serializer.data)



    def patch(self, request):
        product_id = request.query_params.get('pid')
        try:
            product = ShopProducts.objects.get(id=product_id)
        except ShopProducts.DoesNotExist:
            return Response({'error':f'{product_id} is not valid'})
        serializer = UpdateShopProductDetails(product,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'update':serializer.data})
        return Response({'msg':'credentials is needed'})



    def delete(self, request):
        product_id = request.query_params.get('pid')
        try:
            product = ShopProducts.objects.get(id=product_id)
        except ShopProducts.DoesNotExist:
            return Response({'error':f'{product_id} is not valid'})
        productname = product.name
        product.delete()
        return Response({'msg':f'{productname} is deleted'})



class AddProductImages(APIView):
    '''
    products images dynamic size
    '''

    def post(self, request):
        product_id = request.query_params.get('pid')
        if product_id is None:
            return Response({'msg':'pid(product_id) is must'})
        image = AddProductImagesSerializer(data=request.data)
        if image.is_valid(raise_exception=True):
            try:
                product_data = ShopProducts.objects.get(id=product_id)
            except ShopProducts.DoesNotExist:
                print('is not valid')
                return Response({'error':f'{product_id} is not valid'})
            productlist = list()
            for product_image in image.validated_data['image']:
                productlist.append(image.save(image=product_image,productid=product_data))
        return Response({'msg':f'{productlist}'})





class BlockUnblockProducts(APIView):
    '''
    block and unblock products
    '''
    permission_classes=[CustomShopAdminPermission]

    def patch(self, request):
        product_id = request.query_params.get('pid')
        try:
            product = ShopProducts.objects.get(id=product_id)
        except ShopProducts.DoesNotExist:
            return Response({'msg':f'{product_id} is not valid'})
        
        if product.is_available:
            product.is_available = False
            product.save()
            return Response({"confirm":f'{product.name} is blocked'})
        product.is_available = True
        product.save()
        return Response({'confirm':f'{product.name} is unblocked'})
