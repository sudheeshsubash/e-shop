from django.contrib import admin

from .models import *



admin.site.register(CustomUser)
admin.site.register(ShopCategorys)
admin.site.register(ShopDetails)
admin.site.register(ProductsCategorys)
admin.site.register(ShopStaff)
admin.site.register(ShopProducts)
admin.site.register(ProductImages)
admin.site.register(EndUserWishlist)
admin.site.register(EndUserCart)
admin.site.register(ProductVariation)
admin.site.register(EndUserOrders)
admin.site.register(OrderProducts)