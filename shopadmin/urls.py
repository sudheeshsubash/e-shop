from django.urls import path
from . import views


urlpatterns = [
    path('',views.ShopAdminDashBord.as_view(),name='shopdashbord'),
    path('staff/register/',views.StaffRegistrationView.as_view(),name='staff'),
    path('staff',views.ShopStaffView.as_view(),name='staffview'),
    path('staff/<int:staffid>/',views.ShopStaffEdit.as_view(),name='shopstafff'),
    path('login/',views.ShopAdminLogin.as_view(),name='login'),
    path('productcategory/view/',views.ViewAllProductCategoryGlobelAndCustomCategorys.as_view(),name='productcategory'),
    path('productcategory/',views.ProductCategoryAdd.as_view(),name='productcategoryadd'),
    path('productcategory/<int:categoryid>/',views.ProductCategoryEdit.as_view(),name='productcategoryedit'),

]

