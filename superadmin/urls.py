from django.urls import path
from . import views



urlpatterns = [
    path('commonlogin/',views.CommonLogin.as_view(),name='commonlogin'),
    path('loginlogout/',views.LoginSuperAdminEndUserShopAdminShopStaff.as_view(),name='login'),
    path('dashbord/',views.SuperAdminDashBord.as_view(),name='admindashbord'),
    path('<int:shopid>/blockunblock/',views.ShopBlcokUnblock.as_view(),name='blockunblock'),
    path('registration/',views.ShopRegistration.as_view()),
    path('registration/otp/',views.RegistrationOtpConfirm.as_view()),
    path('shopcategory/',views.ShopCategoryView.as_view(),name="shopcategory"),
    path('shopcategory/add/',views.AddShopCategory.as_view(),name="addshopcategory"),
    path('shopcategory/edit/<int:categoryid>/',views.EditShopCategory.as_view(),name="editshopcategory"),
    path('globelcategory/',views.GlobelShopCategory.as_view(),name='globelcategory'),
    path('globelcategory/add/',views.AddGlobelShopCategory.as_view(),name='addglobelcategory'),
    path('globelcategory/<int:categoryid>/edit/',views.EditGlobelShopCategory.as_view(),name='editglobelcategory'),

]
