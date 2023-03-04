from . import views
from django.urls import path


urlpatterns = [
    path('category/',views.AddToCategoryViewEdit.as_view(),name='addviewcategory'),
    path('',views.AddProductViewProductsEditProductDeleteProduct.as_view(),name='addviewdeleteeditproduct'),
    path('blockunblock/',views.BlockUnblockProducts.as_view(),name='blockunblock'),
    path('images/',views.AddProductImages.as_view(),name='productimages')
]
