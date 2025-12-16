from django.shortcuts import render
from rest_framework.views import APIView
from .models import DTODLOG
from .serializers import DtodLogSerializers,CommuterSeraializers, AddCommuterSeraializers
from rest_framework.response import Response 
from datetime import datetime
from cab_services.models import Batch, cab
from user_servcies.models import commuter, Driver
from .utils import * 
from rest_framework import status
from .enumrats import D2dLogStaus
from django.core.cache import cache
# Create your views here.

class RunningBatches(APIView):
    def get(self, request,admin_code, format=None):
        # Reterive 
        batch_ids = Batch.objects.filter(adminCode=admin_code).values_list('id', flat=True)
    
    # Convert the queryset to a list    
        batch_ids_list = list(batch_ids)
        running_batches = DTODLOG.objects.filter(
            tripDate = datetime.now().strftime('%Y-%m-%d'),
            isActive = True,
            batchId__in = batch_ids_list,
            endTime__isnull=True
        )

        seralizre = DtodLogSerializers(running_batches, many=True)
        return Response(seralizre.data,status=status.HTTP_200_OK)
    
class ReturnTrip(APIView):

    def get(self,reqeuest,batch_id,foramt=None):
        
        try:
            batch_data = get_batch_data(batch_id)
            
        except:
            return Response('Error While Fetching Batch Data',status=status.HTTP_204_NO_CONTENT)
        
        
        commuter_data = commuter.objects.prefetch_related("userId").filter(
            batchId=batch_data.pk, isComing=True
        )
          
        serailizer = CommuterSeraializers(commuter_data,many=True)
        
        return Response(serailizer.data,status=status.HTTP_200_OK)

class AddCommuter(APIView):
    def post(Self,request,format=None): 
        serailized_data = AddCommuterSeraializers(data=request.data)
        if serailized_data.is_valid():
            batch_id:AddCommuterSeraializers = serailized_data.data['batch_id']
            commuter_id:AddCommuterSeraializers = serailized_data.data['commuter_id']
            cab_capacity = get_cab_capcity(batch_id)
            current_cache_data:set = get_cache_data(
                batch_id
            )
            current_capcaity = capcaity_check(
                cab_capacity,len(current_cache_data)
            )
            if current_capcaity > 0:
                add_cache_data(
                    batch_id,commuter_id
                )
                turn_off_iscomming(commuter_id)

                return Response("commuter added",status=status.HTTP_201_CREATED)
            else:  
                return Response("out of capcaity",status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Invalid Data",status=status.HTTP_400_BAD_REQUEST)

class CheckD2dLogStatus(APIView):

    def get(self,request,batch_id,foramt=None):
        try:
            d2d_log_data = get_d2d_log_data(batch_id)
        except Exception as e:
            print("E")
            return Response(str(e))
        print(d2d_log_data)
        if d2d_log_data.endTime:
            return Response("3")
        else:
            return Response("2")
        
class CacheData(APIView):
    def get(self,request,batch_id,format=None):
        cache_data = get_cache_data(batch_id)
        cab_capacity = get_cab_capcity(batch_id)
        current_capacity = capcaity_check(
                cab_capacity,len(cache_data)
            )
        return Response({"commuter_list":list(cache_data),"total_capacity":cab_capacity,"current_capacity":current_capacity},status=status.HTTP_200_OK)


class CleareCacheData(APIView):
    def get(self,request,batch_id,format=None):
        clear_cache(batch_id)
        return Response({},status=status.HTTP_200_OK)

class RemoveCacheData(APIView):
    def post(self,request,format=None):
        serailized_data = AddCommuterSeraializers(data=request.data)
        if serailized_data.is_valid():
            batch_id:AddCommuterSeraializers = serailized_data.data['batch_id']
            commuter_id:AddCommuterSeraializers = serailized_data.data['commuter_id']
            remove_cache_data(batch_id,commuter_id)
            return Response("commuter removed",status=status.HTTP_200_OK)
        else:
            return Response("Invalid Data",status=status.HTTP_400_BAD_REQUEST)
