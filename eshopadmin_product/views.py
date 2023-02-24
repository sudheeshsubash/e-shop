from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from admin_app1.tokens_permissions import CustomShopAdminPermission,get_decoded_payload
from .serializers import ShopCategorySerializers,ShopCategorys,ShopProductSerializers,UpdateShopProductDetails
from .serializers import UpdateShopProductImages
from rest_framework import status
from .models import ShopProducts
from admin_app1.paginations import CustomPageNumberPagination



@api_view(['POST','GET'])
@permission_classes([CustomShopAdminPermission])
def add_category(request):
    '''
    add new category to database
    '''
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
    '''
    add new product to database based on the shop_id
    only valid shopadmin can add product
    '''
    serializer = ShopProductSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        decoded_token = get_decoded_payload(request)
        product = serializer.save(decoded_token['user_id'])
        return Response({'msg':f'{product} created'},status=status.HTTP_201_CREATED)
    return Response({'msg':'not done'},status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([CustomShopAdminPermission])
def view_all_product(request):
    '''
    view all products for shopadmin 
    pagination is added
    '''
    if request.method == 'GET':
        pagination = CustomPageNumberPagination()
        pagination_serializer = ShopProductSerializers(pagination.paginate_queryset(ShopProducts.objects.all(),request),many=True)
        return pagination.get_paginated_response(pagination_serializer.data)



@api_view(['PATCH'])
@permission_classes([CustomShopAdminPermission])
def edit_products_details(request,id):
    '''
    update only product details
    with valid eshopadmin
    '''
    try:
        product = ShopProducts.objects.get(id=id)
    except ShopProducts.DoesNotExist:
        return Response({"msg':'product is does't exits"},status=status.HTTP_404_NOT_FOUND)
    
    serializer = UpdateShopProductDetails(product,data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({'update':serializer.data})
    return Response({'msg':'credentials is needed'})



@api_view(['PATCH'])
@permission_classes([CustomShopAdminPermission])
def update_products_images(request,id):
    '''
    update only product images
    with valid eshopadmin
    '''
    try:
        product = ShopProducts.objects.get(id=id)
    except ShopProducts.DoesNotExist:
        return Response({"msg':'product is does't exits"},status=status.HTTP_404_NOT_FOUND)
    
    serializer = UpdateShopProductImages(product,data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response({'update':serializer.data})
    return Response({'msg':'credentials is needed'})




@api_view(['GET'])
@permission_classes([CustomShopAdminPermission])
def block_products(request,id):
    if request.method == 'GET':
        product = ShopProducts.objects.get(id=id)
        product.is_available = False
        product.save()
        return Response({'msg':f'{product} blocked'})



@api_view(['GET'])
@permission_classes([CustomShopAdminPermission])
def un_block_products(request,id):
    if request.method == 'GET':
        product = ShopProducts.objects.get(id=id)
        product.is_available = True
        product.save()
        return Response({'msg':f'{product} unblocked'})