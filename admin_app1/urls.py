from django.urls import path
from . import views

urlpatterns = [
    path('view/',views.custome_user_view,name='user'),
    path('admin/login/',views.login),
]
