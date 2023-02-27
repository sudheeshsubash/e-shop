
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('superadmin/',include('admin_app1.urls')),
    path('eshopadmin/',include('eshopadmin_app1.urls')),
    path('eshopadmin/product/',include('eshopadmin_product.urls')),
    path('shopstaff/',include('shop_staff.urls')),
    path('enduser/',include('enduser_app1.urls')),
    path('enduser/products/',include('enduser_product.urls')),
    path('orders/',include('enduser_orders.urls')),
]
