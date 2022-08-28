from django.core.validators import MinValueValidator, FileExtensionValidator
from django.db import models
import decimal
# Create your models here.
from django.db.models.signals import post_save, pre_delete

from restrant.models import RestaurantProfile, RestaurantBranches, BranchesProfile


def menu_path(instance, filename):
    return 'Menu/{0}/{1}'.format(instance.name, filename)
def cat_path(instance, filename):
    return 'Category/{0}/{1}'.format(instance.name, filename)

class MenusCategory(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    name_la = models.CharField(max_length=100, null=True, blank=True)
    photo = models.FileField(null=True, upload_to=cat_path,
                             validators=[FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    def __str__(self):
        return self.name


class MenusName(models.Model):
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(MenusCategory, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.category.name

class MenusItems(models.Model):
    menu = models.ForeignKey(MenusName, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(MenusCategory, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    name_la = models.CharField(max_length=100, null=True, blank=True)
    describe = models.TextField(null=True, blank=True)
    describe_la = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True,
                                blank=True, validators=[MinValueValidator(decimal.Decimal('0.00'))])
    photo = models.FileField(null=True, upload_to=menu_path,
                             validators=[FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    def __str__(self):
        return self.name


class BranchMenu(models.Model):
    branch = models.ForeignKey(BranchesProfile, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(MenusName, on_delete=models.CASCADE, null=True)

def brnchMenuAdd(sender, instance, created, *args, **kwargs):
    if created:
        get_menu = MenusName.objects.get(branchmenu=instance)
        get_items = MenusItems.objects.filter(menu=get_menu)
        for i in get_items:
            BranchesMenusItems.objects.create(
                branch_menu=instance,category=instance.category,menu=i
            )
post_save.connect(brnchMenuAdd, sender=BranchMenu)
class BranchesMenusItems(models.Model):
    branch_menu = models.ForeignKey(BranchMenu, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(MenusName, on_delete=models.CASCADE, null=True)
    menu = models.ForeignKey(MenusItems, on_delete=models.CASCADE, null=True)
    avalb = models.BooleanField(default=True)

