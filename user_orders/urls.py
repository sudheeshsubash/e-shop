from django.urls import path
from . import views



urlpatterns = [
    path('',views.OnlinePlaceOrder.as_view(),name='placeorder'),
    
]
