from django.urls import path,re_path
from . import views



urlpatterns = [
    path('registration/otp/',views.RegistrationOtpConfirm.as_view(),name='otpconfirm'),
    path('registration/',views.UserRegistration.as_view(),name='registration'),
    path('login/',views.LoginUser.as_view(),name='login'),
    path('products/',views.ViewAllProductsForUser.as_view(),name='viewallproduct'),
    path('<int:productid>/',views.ViewProductsDetails.as_view(),name='viewproductdetails'),
    path('cart/',views.AllCartViewGuestUserAuthenticatedUser.as_view(),name='allcart'),
    path('<int:productid>/cart/',views.UserAddProductToCart.as_view(),name='addtocart'),
    path('cart/<int:cartid>/',views.QuantityDelete.as_view(),name='quantity'),
    path('wishlist/',views.AllWishlistView.as_view(),name='allwishlist'),
    path('<int:productid>/wishlist/',views.AddToWishlist.as_view(),name='addtowishlist'),
    path('wishlist/<int:wishlistid>/',views.EditWishlist.as_view(),name='editwishlist'),
    path('wishlist/cart/',views.WishlistToCart.as_view(),name='wishlitocart')
]
