from django.urls import path
from . import views


urlpatterns = [
    path('view/',views.ViewAllProductsBasedOnShopId.as_view(),name='shopproduct'),
    path('',views.ShopProductsAdd.as_view(),name='addproduct'),
    path('<int:productid>/',views.ShopProductsEdit.as_view(),name='viewproductdetails'),
    path('<int:productid>/image<int:imageid>/',views.ShopProductImageEdit.as_view(),name='productimageedit'),
    path('<int:productid>/image/',views.AddProductImage.as_view(),name='productimage'),
    path('stock/',views.ViewAllProductStock.as_view(),name='productstock'),
    path('stock/<int:productid>/',views.AddProductStock.as_view(),name='addproductstock'),
    

]
