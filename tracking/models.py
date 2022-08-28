import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models import Avg, F
from django.db.models.signals import post_save
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from cart.models import Orders, CostumerProfile, OrderProducts
from restrant.models import RestaurantProfile, BranchesProfile


class OrderTracking(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.ForeignKey(CostumerProfile, on_delete=models.SET_NULL, null=True, blank=True)
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, null=True)
    branch = models.ForeignKey(BranchesProfile, on_delete=models.CASCADE, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    status = models.CharField(max_length=20, blank=True, null=True, )
    create_date = models.DateTimeField(auto_now_add=True)
    start_time = models.PositiveIntegerField(blank=True, null=True, )
    process_date = models.PositiveIntegerField(blank=True, null=True, )
    end_date = models.PositiveIntegerField(blank=True, null=True, )


class BranchRate(models.Model):
    restaurant = models.ForeignKey(RestaurantProfile, on_delete=models.CASCADE, null=True)
    branch = models.ForeignKey(BranchesProfile, on_delete=models.CASCADE, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    process_date = models.PositiveIntegerField(blank=True, null=True, )
    end_date = models.PositiveIntegerField(blank=True, null=True, )
    create_date = models.DateTimeField(auto_now_add=True)


class NotifUser(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False, null=True, )
    title = models.CharField(max_length=250, blank=True, null=True, )
    body = models.CharField(max_length=250, blank=True, null=True, )


def trackOrders(sender, instance, *args, **kwargs):
    if instance.status == 'PAID':
        NotifUser.objects.create(name=instance.name.name, title=instance.transaction_id, body='Order Received')
        NotifUser.objects.create(name=instance.branch.user, title=instance.transaction_id, body='New Order')
        time = int(datetime.datetime.now().timestamp())
        OrderTracking.objects.create(order=instance, name=instance.name, restaurant=instance.restaurant
                                     , branch=instance.branch, status=instance.status, start_time=time)
        get_orderIt = OrderProducts.objects.filter(order=instance)
        htmly = get_template('email.html')
        d = {'order': instance, 'sub': get_orderIt}
        subject, from_email, to = 'MenuLess Invoice', settings.EMAIL_HOST_USER, instance.name.name.email
        text_content = 'This is an important message.'
        html_content = htmly.render(d)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    if instance.status == 'PROCESS':
        NotifUser.objects.create(name=instance.name.name, title=instance.transaction_id, body='Processing your Order')
        obj = OrderTracking.objects.get(order=instance)
        obj.process_date = int(datetime.datetime.now().timestamp())
        obj.save()

    if instance.status == 'COMPLETE' and not instance.is_rate:
        NotifUser.objects.create(name=instance.name.name, title=instance.transaction_id, body='Order is Ready')
        obj = OrderTracking.objects.get(order=instance)
        t1 = obj.start_time
        t2 = obj.process_date
        t3 = int(datetime.datetime.now().timestamp())
        p_time = (t2 - t1)
        e_time = (t3 - t2)
        obj.process_date = p_time
        obj.end_date = e_time
        obj.save()
        end_brch = OrderTracking.objects.filter(branch=instance.branch).aggregate(product__end_date=Avg('end_date'))[
            'product__end_date']
        pro_brch = OrderTracking.objects.filter(branch=instance.branch).aggregate(product__process_date=Avg('process_date'))[
            'product__process_date']
        gt_br, create = BranchRate.objects.get_or_create(restaurant=instance.restaurant
                                     ,branch=instance.branch)
        gt_br.end_date=end_brch
        gt_br.process_date=pro_brch
        gt_br.save()
    if instance.status == 'CANCELLED':
        OrderTracking.objects.create(order=instance, name=instance.name, restaurant=instance.restaurant
                                     , branch=instance.branch, status=instance.status)
    if instance.status == 'LOST':
        OrderTracking.objects.create(order=instance, name=instance.name, restaurant=instance.restaurant
                                     , branch=instance.branch, status=instance.status)
    if instance.is_rate:
        rate = Orders.objects.filter(branch=instance.branch, is_rate=True).aggregate(product__rate=Avg('rate'))[
            'product__rate']
        gt_br, create = BranchRate.objects.get_or_create(restaurant=instance.restaurant
                                     ,branch=instance.branch)
        gt_br.rate=rate
        gt_br.save()

post_save.connect(trackOrders, sender=Orders)


class WebContact(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    mail = models.CharField(max_length=200, null=True, blank=True)
    msg = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

def webContctMsg(sender, instance,created, *args, **kwargs):
    if created:
        htmly = get_template('webmsg.html')
        d = {'order': instance,}
        subject, from_email, to = 'Web contact', settings.EMAIL_HOST_USER, 'webcontact@menu-less.com'
        text_content = 'This is an important message.'
        html_content = htmly.render(d)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

post_save.connect(webContctMsg, sender=WebContact)
