from django.contrib import admin
from django.urls import path,include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,TokenRefreshView
)

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Documentation')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/',include('superadmin.urls')),
    path('api/shop/',include('shopadmin.urls')),
    path('api/shop/product/',include('shopadmin_product_management.urls')),
    path('api/user/',include('user.urls')),
    path('api/user/order/',include('user_orders.urls')),
    
]
