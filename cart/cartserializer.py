from rest_framework import serializers

from menu.models import BranchMenu
from restrant.models import FoodCourt, RestaurantBranches
from .models import *


class UserinSerializer(serializers.Serializer):
    key = serializers.CharField()
    name = serializers.CharField()

class RateSerializer(serializers.Serializer):
    rest = serializers.CharField()
    id = serializers.CharField()
class FoodCourtSerializer(serializers.ModelSerializer):
    restaurant = serializers.SerializerMethodField('get_restaurant')
    branch = serializers.SerializerMethodField('get_branch')

    class Meta:
        model = FoodCourt
        fields = ['id', 'restaurant', 'branch']

    def get_restaurant(self, obj):
        return {
            'name': obj.restaurant.trade_name,
            'logo': obj.restaurant.logo.url,
        }

    def get_branch(self, obj):
        return {
            'branch': obj.branch.id,
        }


class FoodResturantSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField('get_category')

    class Meta:
        model = BranchMenu
        fields = ['id', 'category', ]

    def get_category(self, obj):

        user_id = self.context.get("lang")
        if user_id == 'ar':
            return {
                "photo": obj.category.category.photo.url,
                "name": obj.category.category.name_la
            }
        return {
            "name": obj.category.category.name,
            "photo": obj.category.category.photo.url,
        }


class OrderSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField('get_data')
    name = serializers.SerializerMethodField('get_name')
    rate = serializers.SerializerMethodField('get_rate')
    code = serializers.SerializerMethodField('get_code')
    create_date = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)
    class Meta:
        model = Orders
        fields = ['id','table_no', 'data', 'note', 'name','rate','code','create_date']

    def get_data(self, obj):
        return {
            "ItemsCount": obj.get_cart_items,
            "ItemsSubtotal": obj.get_cart_sub_total,
            "Itemstotal": obj.get_cart_total,
            "Itemstax": obj.get_cart_tax,
            "Itemsservice": obj.get_cart_service,
            "symbl": 'AED',
        }
    def get_name(self,obj):
        return {
            "name":obj.name.name.get_full_name(),
            "phone" : obj.name.phone
        }
    def get_rate(self,obj):
        return{
            "rest":obj.restaurant.trade_name,
            "logo":obj.restaurant.logo.url,

        }
    def get_code(self,obj):
        return {
            "code":obj.qr_code.url
        }


class OrderProductsSerializer(serializers.ModelSerializer):
    product_data = serializers.SerializerMethodField(read_only=True)
    total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderProducts
        fields = ['id', 'price', 'quantity', 'product_data', 'total']

    def get_product_data(self, obj):
        user_id = self.context.get("lang")
        if user_id == 'ar':
            return {
                "name": obj.menu.menu.name_la,
                "photo": obj.menu.menu.photo.url
            }
        return {
            "name": obj.menu.menu.name,
            "photo": obj.menu.menu.photo.url,
        }

    def get_total(self, obj):
        return {
            "total": obj.get_total,
        }


class BranchMenuSerializer(serializers.ModelSerializer):
    menu = serializers.SerializerMethodField('get_menu')

    class Meta:
        model = BranchesMenusItems
        fields = ['id', 'menu', ]

    def get_menu(self, obj):
        user_id = self.context.get("lang")
        if user_id == 'sd':
            return {
                "name": obj.menu.name_la,
                "photo": obj.menu.photo.url,
                "describe": obj.menu.describe_la,
                "price": obj.menu.price,
                "symbl": 'AED',
            }
        return {
            "name": obj.menu.name,
            "photo": obj.menu.photo.url,
            "describe": obj.menu.describe,
            "price": obj.menu.price,
            "symbl": 'AED',
        }


# Resturant
class AllRestOrdersSerializer(serializers.ModelSerializer):
    create_date = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)
    branch = serializers.SerializerMethodField('get_branch')
    user = serializers.SerializerMethodField('get_user')

    class Meta:
        model = Orders
        fields = ['id', 'transaction_id', 'status', 'payment_sys','user', 'branch','total', 'create_date']

    def get_branch(self, obj):
        return {
            "name": obj.branch.name,
        }
    def get_user(self, obj):
        return {
            "name": obj.name.name.get_full_name(),
            "phone": obj.name.phone,
        }

class AllMainOrdersSerializer(serializers.ModelSerializer):
    # create_date = serializers.DateTimeField(format="%Y-%m-%d", required=False, read_only=True)
    user = serializers.SerializerMethodField('get_user')
    detail = serializers.SerializerMethodField('get_detail')
    restaurant = serializers.SerializerMethodField('get_restaurant')

    class Meta:
        model = Orders
        fields = ['id','restaurant', 'transaction_id','table_no','note','sub_total','total','service','tax_amount', 'items','detail', 'payment_sys', 'user','status']

    def get_user(self, obj):
        return {
            "name": obj.name.name.get_full_name(),
            "phone": obj.name.phone,
        }

    def get_detail(self,obj):
        get_menu = OrderProducts.objects.filter(order=obj)
        data = AllOrdersSerializer(get_menu, many=True).data
        return data
    def get_restaurant(self,obj):
        return {
            "rest":obj.restaurant.trade_name
        }



class AllOrdersSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('get_items')
    total = serializers.SerializerMethodField('get_total')

    class Meta:
        model = OrderProducts
        fields = ['id', 'price', 'quantity', 'items', 'total']

    def get_items(self, obj):
        user_id = self.context.get("lang")
        if user_id == 'sd':
            return {
                "photo_data": obj.menu.menu.photo.url,
                "name": obj.menu.menu.name_la,
                "category": obj.menu.menu.category.name_la,
                "describe": obj.menu.menu.describe_la,
            }
        return {
            "photo_data": obj.menu.menu.photo.url,
            "name": obj.menu.menu.name,
            "category": obj.menu.menu.category.name,
            "describe": obj.menu.menu.describe,
        }

    def get_total(self, obj):
        return {
            "total": obj.get_total
        }
