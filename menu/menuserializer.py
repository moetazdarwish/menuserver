from rest_framework import serializers
from .models import *

class MenuCategory(serializers.ModelSerializer):
    data = serializers.SerializerMethodField('get_photo')

    class Meta:
        model = MenusCategory
        fields = ['id','data']

    def get_photo(self,obj):
        user_id = self.context.get("lang")
        if user_id == 'sd':
            return {
                "photo": obj.photo.url,
                "name": obj.name_la
            }
        return {
            "photo" : obj.photo.url,
            "name": obj.name
        }


class MenuRestCategorySerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField('get_photo')

    class Meta:
        model = MenusName
        fields = ['id','data']

    def get_photo(self,obj):
        user_id = self.context.get("lang")
        if user_id == 'sd':
            return {
                "photo": obj.category.photo.url,
                "name": obj.category.name_la
            }
        return {
            "photo" : obj.category.photo.url,
            "name": obj.category.name
        }

class MenuRestItemsSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField('get_photo')

    class Meta:
        model = MenusItems
        fields = ['id','name','name_la','describe','describe_la','price','data']

    def get_photo(self,obj):
        return {
            "photo" : obj.photo.url,
        }

class BranchesListSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField('get_data')

    class Meta:
        model = BranchesProfile
        fields = ['id', 'name', 'data']

    def get_data(self, obj):
        get_menu = MenusName.objects.filter(restaurant=obj.restaurant)
        Menu = MenuRestCategorySerializer(get_menu, many=True).data
        return Menu

class MenuBrchCategorySerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField('get_photo')

    class Meta:
        model = BranchMenu
        fields = ['id','data']

    def get_photo(self,obj):
        user_id = self.context.get("lang")
        if user_id == 'sd':
            return {
                "photo": obj.category.category.photo.url,
                "name": obj.category.category.name_la
            }
        return {
            "photo" : obj.category.category.photo.url,
            "name": obj.category.category.name
        }

class MenuBrchItemsSerializer(serializers.ModelSerializer):

    items = serializers.SerializerMethodField('get_items')

    class Meta:
        model = BranchesMenusItems
        fields = ['id','items','avalb']
    def get_items(self,obj):
        return {
            "photo": obj.menu.photo.url,
            "name": obj.menu.name,
            "name_la": obj.menu.name_la,
            "describe": obj.menu.describe,
            "describe_la": obj.menu.describe_la,
            "price": obj.menu.price,
        }