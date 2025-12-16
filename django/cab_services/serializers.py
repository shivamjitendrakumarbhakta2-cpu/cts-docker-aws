from rest_framework import serializers

from .models import Routes,cab, Batch, pickUpPoints


class customRouteNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = ['routeName']

class CustomPickUpPointInLineSerializer(serializers.ModelSerializer):
    routeId=customRouteNameSerializer()
    class Meta:
        model = pickUpPoints
        fields =['inLine','pickUpPointName','routeId']

class customRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = ["id","routeName"]

class CustomDtodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id','batchName']

class customBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ["id","batchName","end_time","batchTime","startDate","endDate"]

class customPOPSerializer(serializers.ModelSerializer):
    routeId = customRouteSerializer()
    
    class Meta:
        model = pickUpPoints
        fields = ["id","pickUpPointName", "routeId","inLine"]

class customCabSerializer(serializers.ModelSerializer):
    routeId = customRouteSerializer()

    class Meta:
        model = cab
        fields = ["id","regNumber","capacity", "routeId","km"]

class routeSerailizers(serializers.ModelSerializer):
    class Meta:
        model = Routes
        fields = "__all__"
    
class cabSerializers(serializers.ModelSerializer):
    
  
    class Meta:
        model=cab
        fields = "__all__"

class batchSerializers(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = "__all__"

class pickUpPointSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = pickUpPoints
        fields ="__all__"