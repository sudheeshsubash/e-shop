from django.urls import path
from . import views


urlpatterns = [
     path('payment/',views.payment_with_razopay,name='payment'),
     path('checkout/',views.OrderCheckOut.as_view(),name='checkout'),
     
]
