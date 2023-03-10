from django.urls import path
from . import views

urlpatterns = [
    path('',views.ShopAdminDashBord.as_view(),name='shopdashbord'),
    path('registration/',views.ShopRegistration.as_view(),name='shopregistration'),
    path('registration/otp/',views.RegistrationOtpConfirm.as_view(),name='shopregistration'),
    path('product/category/',views.ViewAllProductCategoryGlobelAndCustomCategorys.as_view(),name='productcategory'),
    path('product/category/editadd/',views.CustomizeProductCategoryOrEditAddCategory.as_view(),name='addedit'),

]
