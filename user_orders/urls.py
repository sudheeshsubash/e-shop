from django.urls import path
from . import views



urlpatterns = [
    path('online/',views.OnlinePlaceOrder.as_view()),
    path('address/',views.AddUserAddress.as_view(),name='address'),
    path('cash/',views.CashOnPlaceOrder.as_view(),name='cashonplaceorder'),
    
]
