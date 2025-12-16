from rest_framework import serializers
from .models import commuter, subAdmin, Driver
from cab_services.serializers import customRouteSerializer, customPOPSerializer, customCabSerializer, customBatchSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginSerializer(serializers.Serializer):
    mobileNumber = serializers.CharField(max_length=100)
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


### Model Serializer
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



# Custom serializer

# User
        
class customUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","first_name", "last_name","username","mobileNumber"]
    
class CustomUserContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','mobileNumber','username']

# class CustomReturns
# class CustromUserMobileNumberSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['mobileNumber']
# sub Amdin
        
class SubAdminUserSerailizers(serializers.ModelSerializer):
    userId = CustomUserContactSerializer()
    class Meta:
        model = subAdmin
        fields = ['userId']

#Driver

class customDriverSerializer(serializers.ModelSerializer):
    userId = customUserSerializer()
    batchId = customBatchSerializer()
    cabId = customCabSerializer()
    adminCode = SubAdminUserSerailizers()
    class Meta:
        model = Driver
        fields = ["batchId", "cabId", "userId", "id","adminCode"]

class DriverUserSerailizers(serializers.ModelSerializer):
    userId = CustomUserContactSerializer()
    class Meta:
        model = Driver
        fields = ['userId']

class DriverBatchSerailizers(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['None']

# Commuter

class customCommuterSerializer(serializers.ModelSerializer):
    userId = customUserSerializer()
    batchId = customBatchSerializer()
    popId = customPOPSerializer()
    cabId = customCabSerializer()
    # driver_data = DriverUserSerailizers()
    adminCode = SubAdminUserSerailizers()
    class Meta:
        model = commuter
        fields = [ "batchId","collegeName", "id", "userId","popId","cabId","isComing","adminCode"]

# class D2dLogCommuterSeralizer(serializers.ModelSerializer)
    
#     class Meta:
