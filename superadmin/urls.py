from django.urls import path
from . import views



urlpatterns = [
    
    path('loginlogout/',views.LoginSuperAdminEndUserShopAdminShopStaff.as_view(),name='login'),
    path('dashbord/',views.SuperAdminDashBord.as_view(),name='admindashbord'),
    path('blockunblock/',views.ShopBlcokUnblock.as_view(),name='blockunblock'),
    path('shopcategory/',views.ShopCategoryOrMainClassification.as_view(),name='shopcategory'),
    path('shopcategory/addedit/',views.CustomizeShopCategoryOrMainCategory.as_view(),name='customshopcategory'),

]
