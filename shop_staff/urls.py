from django.urls import path
from . import views


urlpatterns = [
    path('login/',views.LoginStaff.as_view(),name='orderview'),
    path('orders/',views.ViewAllOrders.as_view(),name='allview'),
    path('order/<int:orderid>/',views.ViewOrderDetails.as_view(),name='details'),
    path('order/<int:orderid>/status/',views.ConfirmOrderOrChangeStatus.as_view(),name='details'),


]
