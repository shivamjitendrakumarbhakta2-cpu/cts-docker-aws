from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView

from rest_framework.decorators import api_view
from .models import Routes, Batch, pickUpPoints, cab
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    routeSerailizers,
    batchSerializers,
    pickUpPointSerializers,
    cabSerializers,
)


## Class For Batch Get All and POST
class batch(APIView):
    def get(self, request, format=None):
        batch = Batch.objects.all()
        seralizer = batchSerializers(batch, many=True)
        return Response(seralizer.data)

    def post(self, request, format=None):
        batch = batchSerializers(data=request.data)
        if batch.is_valid():
            batch.save()
            return Response("BATCH CREATED")
        else:
            return Response("ERROR WHILE CREATIN BATCH")


# Class For Single Batch GET,PATCH,DELETE
class batchs(APIView):
    def get(self, request, pk, format=None):
        data = Batch.objects.get(pk=pk)
        serializer = batchSerializers(data)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        batch_data = Batch.objects.get(pk=pk)
        seralizer = batchSerializers(batch_data, data=request.data, partial=True)
        if seralizer.is_valid():
            seralizer.save()
            return Response("BATCH UPDATED")

    def delete(self, request, pk, format=None):
        batch = Batch.objects.get(pk=pk)
        batch.delete()
        return Response("BATCH DELETED")


## Class For Route GET all and POST
class route(APIView):
    def get(self, request, format=None):
        route = Routes.objects.all()
        seralizre = routeSerailizers(route, many=True)
        return Response(seralizre.data)

    def post(self, request, format=None):
        try:
            routes = routeSerailizers(data=request.data)
            if routes.is_valid():
                routes.save()
                return Response("ROUTE CREATED", status=status.HTTP_201_CREATED)

            else:
                return Response("ERROR WHILE CREATING ROUTE")

        except Exception as e:
            print(e)


# Class For accessing Single Route GET,PATCH,DELETE
class routes(APIView):
    def get(self, request, pk, format=None):
        data = Routes.objects.get(pk=pk)

        print(data.routName)
        try:
            serializer = routeSerailizers(data)
            return Response(serializer.data)
        except Exception as e:
            print(e)

    def patch(self, request, pk, format=None):
        route_data = Routes.objects.get(pk=pk)
        try:
            route = routeSerailizers(route_data, data=request.data, partial=True)
            if route.is_valid():
                route.save()
                return Response(route.data)
            else:
                return Response("ERROR")
        except Exception as e:
            print(e)

    def delete(self, request, pk, format=None):
        route = Routes.objects.get(pk=pk)
        try:
            route.delete()
            return Response("DELETED")
        except Exception as e:
            print(e)


# Class For pickUpPoints Get all And POSt
class pick_up_point(APIView):
    def get(self, request, format=None):
        pick_up_point = pickUpPoints.objects.all()
        print(pick_up_point)
        try:
            serializer = pickUpPointSerializers(pick_up_point, many=True)
            return Response(serializer.data)
        except Exception as e:
            print(e)

    def post(self, request, format=None):
        serializer = pickUpPointSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("PICK UP POINT CREATED")
        else:
            return Response(serializer.errors)


class pick_up_points(APIView):
    def get(self, request, pk, foramt=None):
        pick_up_point = pickUpPoints.objects.get(pk=pk)

        serializer = pickUpPointSerializers(pick_up_point)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        pick_up_point = pickUpPoints.objects.get(pk=pk)
        serizlizer = pickUpPointSerializers(
            pick_up_point, data=request.data, partial=True
        )
        if serizlizer.is_valid():
            serizlizer.save()
            return Response("PICK UP POINT UPDATED")
        else:
            return Response("INALID DATA")

    def delete(self, request, pk, format=None):
        data = pickUpPoints.objects.get(pk=pk)
        data.delete()
        return Response("DATA DELETED")


class Cab(APIView):
    def get(self, request, format=None):
        cab_data = cab.objects.all()
        serailizer = cabSerializers(cab_data, many=True)
        return Response(serailizer.data)

    def post(self, request, format=None):
        try:
            serailizers = cabSerializers(data=request.data)
            if serailizers.is_valid():
                serailizers.save()
                return Response("CAB CREATED")
            else:
                return Response("INVLAID DATA" + str(serailizers.errors))
        except Exception as e:
            print(e)


class Cabs(APIView):
    def get(self, request, pk, format=None):
        cab_data = cab.objects.get(pk=pk)
        serailizers = cabSerializers(cab_data)
        return Response(serailizers.data)

    def delete(self, request, pk, foramt=None):
        cab_data = cab.objects.get(pk=pk)
        cab_data.delete()
        return Response("CAB DELETED")

    def patch(self, request, pk, format=None):
        try:
            cab_data = cab.objects.get(pk=pk)

            print(cab_data)
            serailizers = cabSerializers(cab_data, data=request.data, partial=True)
            print(serailizers)
            if serailizers.is_valid():
                serailizers.save()
                return Response("CAB UPDATED")
            else:
                return Response(serailizers.errors)
        except Exception as e:
            print(e)
