from rest_framework import serializers

from .models import Routes,cab, Batch, pickUpPoints


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

