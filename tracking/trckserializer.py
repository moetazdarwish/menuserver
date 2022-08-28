from rest_framework import serializers
from .models import *





class NotifSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotifUser
        fields = ['id','title', 'body']

class BranchesRatesSerializer(serializers.ModelSerializer):
    branch = serializers.SerializerMethodField('get_branch')
    process_date = serializers.SerializerMethodField('get_process')
    end_date = serializers.SerializerMethodField('get_end')
    class Meta:
        model = BranchRate
        fields = ['id','branch','rate', 'process_date','end_date']

    def get_branch(self,obj):
        return {
            "name" : obj.branch.name
        }
    def get_process(self,obj):
        if obj.process_date is None:
            return {
                "process": "No Data"
            }
        return {
                "process" : round(obj.process_date/60,2)
            }

    def get_end(self,obj):
        if obj.end_date is None:
            return {
                "end": "No Data"
            }
        return {
            "end" : round(obj.end_date/60,2)
        }