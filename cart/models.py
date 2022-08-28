import datetime
from decimal import Decimal

import uuid
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image , ImageDraw

# Create your models here.
from django.db.models.signals import pre_save

from menu.models import BranchesMenusItems
from restrant.models import BranchesProfile, RestaurantProfile

def qrcode_path(instance, filename):
    return 'QRcode/{0}/{1}'.format(instance.branch.name, filename)

class CostumerProfile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)


class Orders(models.Model):
    name = models.ForeignKey(CostumerProfile, on_delete=models.SET_NULL, null=True, blank=True)
    restaurant  = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, null=True)
    branch      = models.ForeignKey(BranchesProfile, on_delete=models.CASCADE, null=True)
    sub_total   = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True,
                                    validators=[MinValueValidator(Decimal('0.00'))])
    service     = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True,
                                  validators=[MinValueValidator(Decimal('0.00'))])
    tax_amount  = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True,
                                     validators=[MinValueValidator(Decimal('0.00'))])
    total       = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True,
                                validators=[MinValueValidator(Decimal('0.00'))])
    items       = models.IntegerField(null=True, blank=True)
    note        = models.TextField(null=True, blank=True, default='No Note')
    table_no    = models.IntegerField(null=True, blank=True)
    coupon      = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    transaction_id = models.CharField(max_length=250,null=True,blank=True)
    payment_sys = models.CharField(max_length=30, blank=True, null=True,)
    tran_ref    = models.CharField(max_length=200, blank=True, null=True,)
    is_rate     = models.BooleanField(default=False, null=True, )
    rate        = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    qr_code = models.FileField(null=True, blank=True, upload_to=qrcode_path,
                               validators=[FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    status      = models.CharField(max_length=20, blank=True, null=True, default='CREATED')
    create_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.transaction_id} '

    class Meta:
        ordering = ['-create_date']

    @property
    def get_cart_total(self):
        orderitems = self.orderproducts_set.all()
        total = sum([item.get_total for item in orderitems]) + self.get_cart_tax + self.get_cart_service
        return total

    @property
    def get_cart_sub_total(self):
        orderitems = self.orderproducts_set.all()
        sub_total = sum([item.get_total for item in orderitems])
        return sub_total

    @property
    def get_cart_tax(self):
        if self.restaurant.vat:
            tax = self.get_cart_sub_total * self.restaurant.tax
            return tax
        else:
            tax = 0
            return tax

    @property
    def get_cart_service(self):
        if self.branch.srv:
            service = self.get_cart_sub_total * self.branch.service
            return service
        else:
            service = 0
            return service

    @property
    def get_cart_items(self):
        orderitems = self.orderproducts_set.all()
        total = sum([item.quantity for item in orderitems])

        return total


def createTransaction_id(sender, instance, *args, **kwargs):
    if instance.transaction_id is None:
        timeTrans = str(datetime.datetime.now().timestamp())[:4]
        codeTrans = (uuid.uuid4().hex)[:7]
        transaction_id = codeTrans+timeTrans
        instance.transaction_id = transaction_id
        qrcode_img = qrcode.make(transaction_id)
        canvas = Image.new('RGB', (380, 380), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr-{transaction_id}' + '.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        instance.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
    if instance.status == 'PAID':
        instance.total = instance.get_cart_total
        instance.sub_total = instance.get_cart_sub_total
        instance.items = instance.get_cart_items
        instance.service = instance.get_cart_service
        instance.tax_amount = instance.get_cart_tax


pre_save.connect(createTransaction_id, sender=Orders)


class OrderProducts(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.SET_NULL, null=True, blank=True)
    menu = models.ForeignKey(BranchesMenusItems, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True, validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True,
                                validators=[MinValueValidator(Decimal('0.00'))])
    status = models.CharField(max_length=50, blank=True, null=True, default='CREATED')
    create_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-create_date']

    @property
    def get_total(self):
        total = self.price * self.quantity
        return total