from django.urls import path
from . import views


urlpatterns = [
    path('register/',views.register_eshop_admin,name='registereshopadmin'),
    path('login/',views.login_eshop_admin,name='logineshopadmin'),
    path('create/staff/',views.create_shop_staff,name='createstaff'),
    path('block/<int:id>/',views.block_shop_staff,name='blockshopstaff'),
    path('unblock/<int:id>/',views.un_block_shop_staff,name='unblockshopstaff'),
    path('enduser/block/<int:id>/',views.block_end_user,name='blockenduser'),
    path('enduser/unblock/<int:id>/',views.un_block_end_user,name='unblockenduser'),

]
