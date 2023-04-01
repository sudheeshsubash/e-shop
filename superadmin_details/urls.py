from django.urls import path
from . import views

urlpatterns = [
    path('password/otp/',views.OtpGenerateAndCheck.as_view(),name='otpgeneratevalidate'),
    path('password/',views.ChangePassword.as_view(),name='changepassword'),

    
]
