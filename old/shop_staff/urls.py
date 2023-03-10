from django.urls import path
from . import views


urlpatterns = [
    path('login/',views.shop_staff_login,name='shopstafflogin'),
]
