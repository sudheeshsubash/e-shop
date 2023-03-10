from django.contrib import admin
from .models import EndUserOrders,OrderProducts

# Register your models here.


admin.site.register(EndUserOrders)
admin.site.register(OrderProducts)