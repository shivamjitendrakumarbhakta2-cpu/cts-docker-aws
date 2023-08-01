from rest_framework import serializers
from .models import commuter, subAdmin, Driver
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)


class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "user_permissions",
            "groups",
            "date_joined",
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
        ]


class customUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


class customCommuterSerializer(serializers.ModelSerializer):
    userId = customUserSerializer()

    class Meta:
        model = commuter
        fields = ["PickUpPoint", "batch_id", "id", "vehicle_Code", "userId"]


class customDriverSerializer(serializers.ModelSerializer):
    userId = customUserSerializer()

    class Meta:
        model = Driver
        fields = ["batch_Id", "cab_Id", "userId"]


class commuterSerializer(serializers.ModelSerializer):
    class Meta:
        model = commuter
        fields = "__all__"


class adminSerializer(serializers.ModelSerializer):
    class Meta:
        model = subAdmin
        fields = "__all__"


class driverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = "__all__"
