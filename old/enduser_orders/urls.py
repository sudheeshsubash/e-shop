from django.urls import path
from . import views


urlpatterns = [
     path('checkoutonline/',views.OrderCheckOutOnlinePurchase.as_view(),name='checkoutonline'),
     path('checkoutcash/',views.OrderCheckOutCashOnPurchase.as_view(),name='checkoutcash'),
     path('vieworders/',views.ViewMyOrder.as_view(),name='vieworders'),
     path('vieworders/products/',views.ViewMyOrderProducts.as_view(),name='orderproducts'),
     
]
