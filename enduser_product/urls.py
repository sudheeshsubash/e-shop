from django.urls import path
from . import views

urlpatterns = [
    path('<int:shopid>/',views.view_all_products,name='viewproducts'),
    path('addtocart/<int:pid>/',views.add_to_cart,name='addtocart'),
    path('increse/<int:cid>/',views.insrese_cart_quantity,name='incresequantity'),
    path('decrese/<int:cid>/',views.decrese_cart_quantity,name='decresequantity'),
    path('removecart/<int:cid>/',views.remove_to_cart,name='removetocart'),
    path('addtowishlist/<int:wid>/',views.add_to_wishlist,name='addtowishlist'),
    path('removewishlist/<int:wid>/',views.remove_to_wishlist,name='removewishlist'),
    path('wishlist/<int:wid>/cart/',views.add_wishlist_to_cart,name='wishlisttocart'),
    
]
