from django.contrib import admin

# Register your models here.
from restrant.models import *

admin.site.register(RestaurantProfile)
admin.site.register(RestaurantBranches)
admin.site.register(BranchesProfile)
admin.site.register(CourtsBranches)
admin.site.register(FoodCourt)
admin.site.register(ResSupport)
admin.site.register(CountryCode)
admin.site.register(SubscriptionPlan)
