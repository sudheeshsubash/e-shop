from django.urls import path
from . import views



urlpatterns = [
    path('loginlogout/',views.LoginSuperAdminEndUserShopAdminShopStaff.as_view(),name='login'),
    path('dashbord/',views.SuperAdminDashBord.as_view(),name='admindashbord'),
    path('<int:shopid>/blockunblock/',views.ShopBlcokUnblock.as_view(),name='blockunblock'),
    path('registration/',views.ShopRegistration.as_view(),name='registrtion'),
    path('registration/otp/',views.RegistrationOtpConfirm.as_view(),name='registrationotp'),
    path('superadmin/shop/<int:shopid>/',views.ShopsDetailsEdit.as_view(),name='shopdetails'),
    path('shopcategory/view/',views.ShopCategoryView.as_view(),name="shopcategory"),
    path('shopcategory/',views.AddShopCategory.as_view(),name="addshopcategory"),
    path('shopcategory/<int:categoryid>/',views.EditShopCategory.as_view(),name="editshopcategory"),
    path('productcategory/view/',views.GlobelShopCategory.as_view(),name='globelcategory'),
    path('productcategory/',views.AddGlobelShopCategory.as_view(),name='addglobelcategory'),
    path('productcategory/<int:categoryid>/',views.EditGlobelShopCategory.as_view(),name='editglobelcategory'),

]
