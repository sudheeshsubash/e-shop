from django.urls import path
from . import views



urlpatterns = [
    path('',views.OnlinePlaceORder.as_view()),
    path('address/',views.AddUserAddress.as_view(),name='address'),
    
]
