from . import views
from django.urls import path


urlpatterns = [
    path('category/add/',views.add_category,name='addproduct'),
    path('add/',views.add_products,name='addproducts'),
    path('viewall/',views.view_all_product,name='viewall'),
    path('<int:id>/update/',views.update_products,name='updateproduct'),

]
