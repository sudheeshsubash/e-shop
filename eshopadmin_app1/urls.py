from django.urls import path
from . import views


urlpatterns = [
    path('register/',views.register_eshop_admin,name='registereshopadmin'),
    path('login/',views.login_eshop_admin,name='logineshopadmin'),
    path('logout/',views.logout_eshop_admin,name='logouteshopadmin'),

]
