from rest_framework import serializers
from .models import *


# user

class USERPROFILESerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField( read_only=True)
    class Meta:
        model = RestaurantProfile
        fields = ['phone', 'address','postal_code','area','city']

    def get_city(self,obj):
        return {
            "city":obj.city,
            "country":obj.country
        }

class PlanSerializer(serializers.Serializer):
    go = serializers.CharField()
    start = serializers.CharField()
    elite  = serializers.CharField()
    symbl  = serializers.CharField()
class RegDataSerializer(serializers.Serializer):
    rate = serializers.CharField()
    symbl = serializers.CharField()
    total = serializers.CharField()
    period = serializers.CharField()
    name = serializers.CharField()
    logo = serializers.CharField()
    key = serializers.CharField()

class LogininSerializer(serializers.Serializer):
    key = serializers.CharField()
    name = serializers.CharField()
    logo = serializers.CharField()

class BranchesSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField( 'get_data')
    class Meta:
        model = BranchesProfile
        fields = ['id','name', 'data','srv','service']

    def get_data(self,obj):
        try:
            crt = FoodCourt.objects.get(branch=obj)
            return {
                "tables": crt.court.tables,
                "trade_name": crt.court.court,
                "type":"mall"
            }
        except:
            return {
                "trade_name": obj.restaurant.trade_name,
                "tables": obj.get_tables,
                "type": "restaurant"
            }

class BranchesTablesSerializer(serializers.ModelSerializer):
    court = serializers.SerializerMethodField('get_court')
    class Meta:
        model = RestaurantBranches
        fields = ['id','court']
    def get_court(self,obj):
        return {
            "branch": obj.branch.id,
            "table_no": obj.table_no,
            "code": obj.table_code,
            "name": obj.branch.name,
            "qr_code": obj.qr_code.url,
            "logo": obj.restaurant.logo.url,
            "rest": obj.restaurant.trade_name,
        }


class CourtTablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtsBranches
        fields = ['id','court', 'tables','code']

class CourtDataSerializer(serializers.ModelSerializer):
    court = serializers.SerializerMethodField('get_court')
    class Meta:
        model = FoodCourt
        fields = ['id','court']
    def get_court(self,obj):
        return {
            "table_no":obj.court.tables,
            "code":obj.court.code,
            "name":obj.court.court,
            "branch":obj.branch.id,
            "qr_code":obj.court.qr_code.url,
            "logo": obj.restaurant.logo.url,
            "rest": obj.restaurant.trade_name,
        }

