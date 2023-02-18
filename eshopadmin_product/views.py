from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from admin_app1.tokens_permissions import CustomShopAdminPermission,get_decoded_payload
from .serializers import ShopCategorySerializers,ShopCategorys,ShopProductSerializers,UpdateShopProductSerializers
from rest_framework import status
from .models import ShopProducts
from admin_app1.paginations import CustomPageNumberPagination



@api_view(['POST','GET'])
@permission_classes([CustomShopAdminPermission])
def add_category(request):
    if request.method == 'POST':
        serializer = ShopCategorySerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'msg':serializer.data},status=status.HTTP_201_CREATED)
        return Response({'msg':'data not valid'},status=status.HTTP_406_NOT_ACCEPTABLE)
    
    if request.method == 'GET':
        category = ShopCategorys.objects.all()
        serializer = ShopCategorySerializers(category,many=True)
        return Response({'categorys':serializer.data})





@api_view(['POST'])
@permission_classes([CustomShopAdminPermission])
def add_products(request):
    serializer = ShopProductSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        decoded_token = get_decoded_payload(request)
        product = serializer.save(decoded_token['user_id'])
        return Response({'msg':f'{product} created'},status=status.HTTP_201_CREATED)
    return Response({'msg':'not done'},status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([CustomShopAdminPermission])
def view_all_product(request):
    if request.method == 'GET':
        pagination = CustomPageNumberPagination()
        pagination_serializer = ShopProductSerializers(pagination.paginate_queryset(ShopProducts.objects.all(),request),many=True)
        return pagination.get_paginated_response(pagination_serializer.data)



@api_view(['PATCH'])
@permission_classes([CustomShopAdminPermission])
def update_products(request,id):
    try:
        product = ShopProducts.objects.get(id=id)
    except ShopProducts.DoesNotExist:
        return Response({"msg':'product is does't exits"},status=status.HTTP_404_NOT_FOUND)
    
    serializer = UpdateShopProductSerializers(product,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'update':serializer.data})
    return Response({'msg':'credentials is needed'})