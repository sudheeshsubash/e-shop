from django.urls import path,re_path
from . import views



urlpatterns = [
    path('product/',views.ViewAllProductsForUser.as_view(),name='viewallproduct'),
    path('cart/',views.AddToCartGuestUserAndAuthenticatedUser.as_view(),name='addtocart'),
    path('wishlist/',views.AddToGueWishliststUserAndAuthenticatedUser.as_view(),name='addtowishlist'),
    path('registration/',views.UserRegistration.as_view(),name='registration'),
    path('registration/otp/',views.RegistrationOtpConfirm.as_view(),name='otpconfirm'),
]
