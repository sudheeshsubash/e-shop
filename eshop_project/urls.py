
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('superadmin/',include('admin_app1.urls')),
    path('eshopadmin/',include('eshopadmin_app1.urls')),
    path('eshopadmin/product/',include('eshopadmin_product.urls')),
    
]
