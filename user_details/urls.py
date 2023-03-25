from django.urls import path
from . import views

urlpatterns = [
    path('password/',views.ChangePassword.as_view(),name='changepassword'),
    path('password/otp/',views.PasswordChangeOtp.as_view(),name='otppassword'),

]
