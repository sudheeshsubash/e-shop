from django.urls import path
from . import views


urlpatterns = [
    path('editadd/',views.ShopProductsAddEditDelete.as_view(),name='editadd'),
    
]
