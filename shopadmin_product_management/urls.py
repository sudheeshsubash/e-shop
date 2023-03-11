from django.urls import path
from . import views


urlpatterns = [
    path('',views.ViewAllProductsBasedOnShopId.as_view(),name='shopproduct'),
    path('editadd/',views.ShopProductsAddEditDelete.as_view(),name='editadd'),
    
]
