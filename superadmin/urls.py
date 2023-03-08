from django.urls import path
from . import views



urlpatterns = [
    
    path('login/',views.LoginSuperAdminEndUserShopAdminShopStaff.as_view(),name='login'),
    path('dashbord/',views.SuperAdminDashBord.as_view(),name='admindashbord'),
    path('blockunblock/',views.ShopBlcokUnblock.as_view(),name='blockunblock'),
    

]
