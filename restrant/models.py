import decimal
from decimal import Decimal
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
import uuid
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
import datetime
# Create your models here.
from django.db.models.signals import post_save, pre_save, pre_delete
from django.template.loader import get_template
from rest_framework.authtoken.models import Token
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


def restaurant_path(instance, filename):
    return 'Restaurant/{0}/{1}'.format(instance.trade_name, filename)


def branch_path(instance, filename):
    return 'Branches/{0}/{1}'.format(instance.branch.name, filename)


def court_path(instance, filename):
    return 'FoodCourt/{0}/{1}'.format(instance.court, filename)


class SubscriptionPlan(models.Model):
    plan = models.CharField(max_length=250, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True, )
    duration = models.PositiveIntegerField(default=30, null=True, blank=True)
    period = models.PositiveIntegerField(default=30, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.plan},{self.id}'


class RestaurantProfile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True, default='No Address')
    symbl = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    terms = models.BooleanField(default=True, null=True, blank=True)
    trade_name = models.CharField(max_length=150, null=True, blank=True)
    logo = models.FileField(null=True, upload_to=restaurant_path,
                            validators=[FileExtensionValidator(['png', 'jpeg', 'jpg'])])
    approve = models.BooleanField(default=False, null=True, )
    plan = models.ForeignKey('SubscriptionPlan', on_delete=models.SET_NULL, null=True, blank=True)
    vat = models.BooleanField(default=False, null=True, )
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True,
                              validators=[MinValueValidator(Decimal('0.00'))])
    service = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True,
                                  validators=[MinValueValidator(Decimal('0.00'))])
    trader_payment = models.BooleanField(default=False, null=True, blank=True)
    payment_profile_id = models.CharField(max_length=20, null=True, blank=True)
    payment_aut = models.TextField(null=True, blank=True)
    until_date = models.DateField(blank=True, null=True)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.trade_name


class CourtsBranches(models.Model):
    court = models.CharField(max_length=50, blank=True, null=True)
    code = models.CharField(max_length=250, blank=True, null=True)
    tables = models.PositiveIntegerField(default=10, blank=True, null=True)
    qr_code = models.FileField(null=True, blank=True, upload_to=court_path,
                               validators=[FileExtensionValidator(['png', 'jpeg', 'jpg'])])

    def save(self, *args, **kwargs):
        code = uuid.uuid4().hex
        self.code = code
        qrcode_img = qrcode.make(code)
        canvas = Image.new('RGB', (380, 380), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.court}' + '.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


def foodCourtCode(sender, instance, *args, **kwargs):
    if instance.code is None:
        code = datetime.datetime.now().timestamp()
        instance.code = code


pre_save.connect(foodCourtCode, sender=CourtsBranches)


class BranchesProfile(models.Model):
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    srv = models.BooleanField(default=False, null=True, blank=True)
    is_branch = models.BooleanField(default=True, null=True)
    service = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True,
                                  validators=[MinValueValidator(Decimal('0.00'))])
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def get_tables(self):
        orderitems = self.restaurantbranches_set.all().count()
        # total = sum([item.table_no for item in orderitems])
        return orderitems


class RestaurantBranches(models.Model):
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, null=True)
    branch = models.ForeignKey(BranchesProfile, on_delete=models.CASCADE, null=True)
    table_no = models.PositiveIntegerField(blank=True, null=True)
    table_code = models.CharField(max_length=250, blank=True, null=True)
    qr_code = models.FileField(null=True, blank=True, upload_to=branch_path,
                               validators=[FileExtensionValidator(['png', 'jpeg', 'jpg'])])

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.table_code)
        canvas = Image.new('RGB', (380, 380), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.table_no}' + '.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


class FoodCourt(models.Model):
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, null=True)
    branch = models.ForeignKey(BranchesProfile, on_delete=models.CASCADE, null=True)
    court = models.ForeignKey(CourtsBranches, on_delete=models.CASCADE, null=True)


class ResSupport(models.Model):
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, null=True, blank=True)
    branch = models.ForeignKey(BranchesProfile, on_delete=models.CASCADE, null=True, blank=True)
    subj = models.CharField(max_length=200, null=True, blank=True)
    question = models.TextField()
    answer = models.TextField()
    cret_date = models.DateTimeField(auto_now_add=True)
def restsupportMsg(sender, instance,created, *args, **kwargs):
    if created:
        htmly = get_template('suprtmail.html')
        d = {'msg': instance,}
        subject, from_email, to = 'Support', settings.EMAIL_HOST_USER, 'support@menu-less.com'
        text_content = 'This is an important message.'
        html_content = htmly.render(d)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

post_save.connect(restsupportMsg, sender=ResSupport)

class CountryCode(models.Model):
    country = models.CharField(max_length=250, blank=True, null=True)
    countrycode = models.CharField(max_length=250, blank=True, null=True)
    currency = models.CharField(max_length=250, blank=True, null=True)
    go_pln = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True, )
    go_period = models.PositiveIntegerField(default=30, null=True, blank=True)
    strt_pln = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True, )
    strt_period = models.PositiveIntegerField(default=30, null=True, blank=True)
    elit_pln = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True, )
    elit_period = models.PositiveIntegerField(default=30, null=True, blank=True)
    bg_pln = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True, )
    bg_period = models.PositiveIntegerField(default=30, null=True, blank=True)
    pyment = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.country


class SubscriptionOrders(models.Model):
    name = models.ForeignKey(RestaurantProfile, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True, )
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True, )
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    transaction_id = models.CharField(max_length=250, null=True, blank=True)
    c_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True, )
    rate = models.DecimalField(max_digits=10, decimal_places=4, default=0.00, null=True, blank=True, )
    symbol = models.CharField(max_length=10, blank=True, null=True, )
    period = models.PositiveIntegerField(default=30, null=True, blank=True)
    tran_ref = models.CharField(max_length=200, blank=True, null=True, )
    status = models.CharField(max_length=20, blank=True, null=True, default='CREATED')
    until_date = models.DateField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)


def OrderTransction(sender, instance, created, *args, **kwargs):
    if instance.status == 'PAID':
        htmly = get_template('subconfirm.html')
        subject, from_email, to = 'MenuLess', settings.EMAIL_HOST_USER, instance.name.name.email
        text_content = 'This is an important message.'
        html_content = htmly

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
post_save.connect(OrderTransction, sender=SubscriptionOrders)


def Tokencreatoruser(sender, instance, created, *args, **kwargs):
    if created:
        Token.objects.get_or_create(user=instance)


post_save.connect(Tokencreatoruser, sender=User)

def NewRestReg(sender, instance, created, *args, **kwargs):
    if created:
        htmly = get_template('restreg.html')
        subject, from_email, to = 'MenuLess', settings.EMAIL_HOST_USER, instance.name.email
        text_content = 'This is an important message.'
        html_content = htmly

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

post_save.connect(NewRestReg, sender=RestaurantProfile)