from django.urls import path
from . import views

urlpatterns = [
    path('changepassword/otp/',views.OtpGenerateAndCheck.as_view(),name='otpgeneratevalidate'),
    
]
