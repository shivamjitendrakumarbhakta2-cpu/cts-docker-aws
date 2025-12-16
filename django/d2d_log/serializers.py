from rest_framework import serializers
from cab_services.serializers import CustomDtodLogSerializer,CustomPickUpPointInLineSerializer

from user_servcies.models import commuter
from user_servcies.Serializers import CustomUserContactSerializer

from .models import DTODLOG

class DtodLogSerializers(serializers.ModelSerializer):
    batchId = CustomDtodLogSerializer()
    class Meta:
        model = DTODLOG
        fields = ['id','batchId']

class CommuterSeraializers(serializers.ModelSerializer):
    
    userId = CustomUserContactSerializer()
    popId = CustomPickUpPointInLineSerializer()
    
    class Meta:
        model = commuter
        fields = ['userId','popId']
        
class AddCommuterSeraializers(serializers.Serializer):
    batch_id = serializers.CharField(required=True)
    commuter_id = serializers.CharField(required=True)

class RemoveCommuterSeraializers(serializers.Serializer):
    batch_id = serializers.CharField(required=True)
    commuter_id = serializers.CharField(required=True)