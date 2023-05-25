from django.contrib import admin
from django.urls import path,include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView


from rest_framework_simplejwt.views import (
    TokenObtainPairView,TokenRefreshView
)

# from rest_framework_swagger.views import get_swagger_view
# schema_view = get_swagger_view(title='API Documentation')

urlpatterns = [
    path('',TemplateView.as_view(template_name='docs.html',extra_context={'schema_url':'apilist'})),
    path('apilist/',get_schema_view(title='apis',description='api docs'),name='apilist'),
    path('admin/', admin.site.urls),
    # path('docs/', schema_view),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('',include('superadmin.urls')),
    path('shop/<int:shopid>/',include('shopadmin.urls')),
    path('shop/<int:shopid>/product/',include('shopadmin_product_management.urls')),
    path('shop/<int:shopid>/user/',include('user.urls')),
    path('shop/<int:shopid>/user/order/',include('user_orders.urls')),
    path('shop/<int:shopid>/user/details/',include('user_details.urls')),
    path('shop/<int:shopid>/staff/',include('shop_staff.urls')),
    path('details/',include('superadmin_details.urls')),
    path('shop/<int:shopid>/product/<int:productid>/',include('user_product.urls')),
    
]
