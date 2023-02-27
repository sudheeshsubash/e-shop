from django.urls import path
from . import views



urlpatterns = [
    path('register/',views.register_new_end_user,name='registerenduser'),
    path('view/',views.view_all_shops_details,name='viewallshop'),
    path('login/',views.login_end_user,name='loginenduser'),

]
