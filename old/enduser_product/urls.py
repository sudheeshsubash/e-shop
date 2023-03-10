from django.urls import path
from . import views

urlpatterns = [

    path('showproducts/',views.ShowAllProductsChoosedShop.as_view(),name='showproducts'),
    path('cart/',views.CartManagementForEndUser.as_view(),name='cartmanagement'),


]
