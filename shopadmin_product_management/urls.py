from django.urls import path
from . import views


urlpatterns = [
    path('view/',views.ViewAllProductsBasedOnShopId.as_view(),name='shopproduct'),
    path('<int:productid>/',views.ShopProductDetails.as_view()),
    path('add/',views.ShopProductsAdd.as_view(),name='addproduct'),
    path('edit/<int:productid>/',views.ShopProductsEdit.as_view(),name='editproduct'),
    path('edit/<int:productid>/image/<int:imageid>/',views.ShopProductImageEdit.as_view(),name='editimage'),

]
