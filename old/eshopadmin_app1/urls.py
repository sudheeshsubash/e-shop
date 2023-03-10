from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter




urlpatterns = [
    path('register/',views.register_eshop_admin,name='registereshopadmin'),
    path('login/',views.login_eshop_admin,name='logineshopadmin'),
    path('logout/',views.logout_eshop_admin,name='logouteshopadmin'),
    path('shopstaff/',views.ShopStaffCreateView.as_view(),name='shopstaff'),
    path('enduserblockunblock/',views.EndUserBlockUnblock.as_view(),name='enduserblockunblock'),
    path('productblockunblock/',views.ProductChageAvailability.as_view(),name='productblockunblock'),
    

]
