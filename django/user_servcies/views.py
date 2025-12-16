from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import commuter, Driver, subAdmin
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from .Serializers import (
    LoginSerializer,
    userSerializer,
    commuterSerializer,
    adminSerializer,
    driverSerializer,
    customCommuterSerializer,
    customCommuterSerializer,
    customDriverSerializer,
    DriverUserSerailizers

)
import uuid
from django.db import transaction

User = get_user_model()
# Create your views here.


class common_user(APIView):
    def get(self, request, foramt=None):
        user = User.objects.all()
        try:
            serializer = userSerializer(user, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)
            return Response(str(serializer.errors))
    
    @transaction.atomic
    def post(self, request, foramt=None):
        if (len(request.data['user']['username'].split(" "))==2):
          request.data["user"]["first_name"],request.data["user"]["last_name"] = request.data["user"]["username"].split(" ")[0],request.data["user"]["username"].split(" ")[1]
        else:
          request.data['user']['first_name'] = request.data["user"]["username"]
          
        request.data["user"]["password"] = make_password(
            request.data["user"]["password"]
        )
        # request.data["user"]["first"]
        user_serailizer = userSerializer(data=request.data["user"])
        
        if user_serailizer.is_valid():
            user = user_serailizer.save()
            # sid = transaction.savepoint()
            request.data["user_data"]["userId"] = user.id
        # user = user_serailizer.save()
        
            

            
            if user.userType == "COMMUTER":
                # print(request.data["user_data"])
                commuter_serilizers = commuterSerializer(data=request.data["user_data"])

                if commuter_serilizers.is_valid():
                    # transaction.savepoint_commit(sid)
                    # user = user_serailizer.save()
            # sid = transaction.savepoint()
                    # request.data["user_data"]["userId"] = user.id
                    commuter_serilizers.save()
                    return Response("commuter created")
                else:
                    # transaction.savepoint_rollback(sid)
                    user.delete()
                    return Response(str(commuter_serilizers.errors))

            elif user.userType == "ADMIN":
                admin_serailizer = adminSerializer(data=request.data["user_data"])
                if admin_serailizer.is_valid():
                    # user = user_serailizer.save()
                    # transaction.savepoint_commit(sid)
                    user.save()
                    admin_serailizer.save()
                    return Response("admin created")
                else:
                    user.delete()
                    # transaction.savepoint_rollback(sid)
                    return Response(str(admin_serailizer.errors))

            elif user.userType == "DRIVER":
                try:
                    # print("DRIVER")
                    driver_serailizer = driverSerializer(data=request.data["user_data"])
                    if driver_serailizer.is_valid():
                        # transaction.savepoint_commit(sid)
                        # user = user_serailizer.save()
                        # user.save()
                        driver_serailizer.save()
                        return Response("driver created")
                    else:
                        user.delete()
                        # transaction.savepoint_rollback(sid)
                        return Response(str(driver_serailizer.errors))
                except Exception as e:
                    print(e)
        else:
            return Response(user_serailizer.errors)


class users(APIView):
    def get(self, request, pk, foramt=None):
        user = User.objects.get(pk=pk)
        serializer = userSerializer(user)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = userSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response("user updated")
            else:
                return Response(str(serializer.errors))
        except Exception as e:
            print(e)

    def delete(self, request, pk, foramt=None):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response("USER DELETED")


class Commuter(APIView):
    def get(self, request, foramt=None):
        commuter_data = commuter.objects.all()
        serializers = commuterSerializer(commuter_data, many=True)
        return Response(serializers.data)


class Commuters(APIView):
    def get(self, request, pk, format=None):
        try:
            commuter_data = commuter.objects.get(userId=pk)
            serializers = customCommuterSerializer(commuter_data)
            return Response(serializers.data)

        except Exception as e:
            return Response(str(e))

    def patch(self, request, pk, format=None):
        # print(f"COMMUTER PACTH CALLED:,{pk}")
        commuter_data = commuter.objects.get(userId=pk)
        serializer = commuterSerializer(commuter_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("commuter updated")
        else:
            return Response(serializer.error_messages)

    def delete(self, request, pk, format=None):
        get_commuter = commuter.objects.get(userId=pk)
        get_commuter.delete()
        return Response("COMMUTER DELETED, PLEASE DETLETE THE USER AS WELL")


class Admin(APIView):
    def get(self, request, foramt=None):
        admin_data = subAdmin.objects.all()
        serializers = adminSerializer(admin_data, many=True)
        return Response(serializers.data)


class Admins(APIView):
    def get(self, request, pk, format=None):
        try:
            admin_data = subAdmin.objects.get(userId=pk)
            serializers = adminSerializer(admin_data)
            return Response(serializers.data)

        except Exception as e:
            return Response("ERROR")

    def patch(self, request, pk, format=None):
        admin_data = subAdmin.objects.get(userId=pk)
        serializer = adminSerializer(admin_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return (serializer.data)
        else:
            return Response(serializer.error_messages)

    def delete(self, request, pk, format=None):
        admin_data = subAdmin.objects.get(userId=pk)
        admin_data.delete()
        return Response("ADMIN DELETED, PLEASE DETLETE THE USER AS WELL")


class custom_admin(APIView):
    def get(self, request, name, pk, fromat=None):
        if name == "commuter":
            adminData = subAdmin.objects.get(pk=uuid.UUID(pk).hex)
            print(adminData)
            commuter_data = commuter.objects.select_related("userId").filter(
                adminCode=adminData
            )

            commuterSerailizer = customCommuterSerializer(commuter_data, many=True)

            return Response(commuterSerailizer.data)
        elif name == "driver":
            driver_data = Driver.objects.select_related("userId").filter(adminCode=pk)
            driverSerailizer = customDriverSerializer(driver_data, many=True)

            return Response(driverSerailizer.data)


class driver(APIView):
    def get(self, request, foramt=None):
        driver_data = Driver.objects.all()
        serializers = customDriverSerializer(driver_data, many=True)
        return Response(serializers.data)



class drivers(APIView):
    def get(self, request, pk, format=None):
        try:
            driver_data = Driver.objects.get(userId=pk)
            serializers = customDriverSerializer(driver_data)
            return Response(serializers.data)

        except Exception as e:
            return Response("ERROR")

    def patch(self, request, pk, format=None):
        driver_data = Driver.objects.get(userId=pk)
        serializer = driverSerializer(driver_data, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("driver updated")
        else:
            return Response(serializer.error_messages)

    def delete(self, request, pk, format=None):
        driver_data = Driver.objects.get(userId=pk)
        driver_data.delete()
        return Response("ADMIN DELETED, PLEASE DETLETE THE USER AS WELL")


class DriverBatch(APIView):
    def get(self,request,batch_id,foramt=None):
        driver_data  = Driver.objects.get(batchId=batch_id)
        driver_contact_detail = DriverUserSerailizers(driver_data)
    
        try:
            
                # driver_contact_detail = DriverUserSerailizers(data=driver_data.id)
            return Response(driver_contact_detail.data)
            
        except Exception as e:
            return Response(str(e))

        


@api_view(["POST"])
def login_user(request):
    if request.user.is_authenticated:
        return Response("USER ALREADY LOGGED IN")
    try:
        serailizer = LoginSerializer(data=request.data)
        print(serailizer)
        if serailizer.is_valid():
            user = authenticate(
                request=request,
                username=serailizer.data["mobileNumber"],
                password=serailizer.data["password"],
            )
            if user is not None:
                try:
                    login(request, user)
                except Exception as e:
                    print("ERROR WHILE LOGIN", e)
                # type: ignore
                return Response(
                    {"user_id": user.id, "user_type": user.userType},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                serailizer.error_messages, status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response(str(e))


@api_view(["POST"])
def logout_user(request):
    try:
        logout(request._request)
        return Response("User Logged Out")
    except Exception as e:
        print(e)
        return Response("ERROR")


