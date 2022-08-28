from django.contrib import admin

# Register your models here.
from tracking.models import *

admin.site.register(OrderTracking)
admin.site.register(BranchRate)
admin.site.register(NotifUser)
admin.site.register(WebContact)