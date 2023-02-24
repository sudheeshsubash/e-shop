from django.urls import path
from . import views

urlpatterns = [
    path('view/',views.custome_user_view,name='user'),
    path('admin/login/',views.login),
    path('block/<int:id>/',views.block_shop,name='blockshop'),
    path('unblock/<int:id>/',views.un_block_shop,name='blockshop'),

]
