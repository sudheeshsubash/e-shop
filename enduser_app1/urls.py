from django.urls import path
from . import views



urlpatterns = [
    path('register/',views.register_new_end_user,name='registerenduser'),
    path('login/',views.login_end_user,name='loginenduser'),
    path('shops/',views.ViewAllShopsDetails.as_view(),name='shops'),
    
]
