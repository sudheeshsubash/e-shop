from django.urls import path,re_path
from . import views



urlpatterns = [
    path('registration/otp/',views.RegistrationOtpConfirm.as_view(),name='otpconfirm'),
    path('registration/',views.UserRegistration.as_view(),name='registration'),
    path('login/',views.LoginUser.as_view(),name='login'),
    path('product/',views.ViewAllProductsForUser.as_view(),name='viewallproduct'),
    path('<int:productid>/view/',views.ViewProductsDetails.as_view(),name='viewproductdetails'),
    path('cart/all/',views.AllCartViewGuestUserAuthenticatedUser.as_view(),name='allcart'),
    path('<int:productid>/add/cart/',views.UserAddProductToCart.as_view(),name='addtocart'),
    path('<int:cartid>/edit/cart/',views.QuantityDelete.as_view(),name='quantity'),
    path('wishlist/all/',views.AllWishlistView.as_view(),name='allwishlist'),
    path('<int:productid>/add/wishlist/',views.AddToWishlist.as_view(),name='addtowishlist'),
    path('<int:wishlistid>/edit/wishlist/',views.EditWishlist.as_view(),name='editwishlist'),
    path('wishlist/cart/',views.WishlistToCart.as_view(),name='wishlitocart')
]
