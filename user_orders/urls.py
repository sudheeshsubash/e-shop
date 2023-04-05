from django.urls import path
from . import views



urlpatterns = [
    path('choosemethod/',views.ChooseAddressAndPaymentType.as_view(),name='chooseaddress'),
    path('type/online/',views.PlaceOrderOnlinePurchase.as_view()),
    path('type/cash/',views.PlaceOrderCashOnPurchase.as_view()),
    path('address/',views.AddUserAddress.as_view()),
    path('view/',views.ViewAllOrders.as_view()),

    
]
