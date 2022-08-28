from django.contrib import admin

# Register your models here.
from cart.models import *

admin.site.register(CostumerProfile)
admin.site.register(Orders)
admin.site.register(OrderProducts)