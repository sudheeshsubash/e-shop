from . import views
from django.urls import path


urlpatterns = [
    path('category/add/',views.add_category,name='addproduct'),
    path('add/',views.add_products,name='addproducts'),
    path('viewall/',views.view_all_product,name='viewall'),
    path('<int:id>/details/update/',views.edit_products_details,name='updateproductdetails'),
    path('<int:id>/images/update/',views.update_products_images,name='updateproductimages'),
    path('<int:id>/block/',views.block_products,name='blockproducts'),
    path('<int:id>/unblock/',views.un_block_products,name='unblockproducts'),

]
