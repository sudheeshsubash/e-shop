from django.urls import path
from . import views

urlpatterns = [
    path('',views.ShopAdminDashBord.as_view(),name='shopdashbord'),
    path('login/',views.ShopAdminLogin.as_view(),name='login'),
    path('productcategory/',views.ViewAllProductCategoryGlobelAndCustomCategorys.as_view(),name='productcategory'),
    path('productcategory/add/',views.ProductCategoryAdd.as_view(),name='productcategoryadd'),
    path('productcategory/edit/<int:categoryid>/',views.ProductCategoryEdit.as_view(),name='productcategoryedit'),

]
