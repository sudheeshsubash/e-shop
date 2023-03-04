from django.urls import path
from . import views

urlpatterns = [
    path('view/',views.show_all_shops_users,name='show'),
    path('admin/login/',views.login),
    path('blockunblock/',views.ShopBlcokUnblock.as_view(),name='blockunblock'),
    

]
