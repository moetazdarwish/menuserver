from django.contrib import admin

# Register your models here.
from menu.models import *

admin.site.register(MenusCategory)
admin.site.register(MenusName)
admin.site.register(MenusItems)
admin.site.register(BranchMenu)
admin.site.register(BranchesMenusItems)