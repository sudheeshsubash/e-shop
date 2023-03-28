from django.urls import path
from . import views


urlpatterns = [
    path('',views.StaffOrderView.as_view(),name='orderview'),
    path('<int:orderid>/',views.ViewOrderDetails.as_view(),name='details'),
    path('<int:orderid>/status/',views.ConfirmOrderOrChangeStatus.as_view(),name='details'),
    
]