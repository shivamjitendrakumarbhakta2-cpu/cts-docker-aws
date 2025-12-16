from cab_services.models import Batch
from django.shortcuts import get_object_or_404
from user_servcies.models import commuter
from .serializers import CustomDtodLogSerializer
from .models import DTODLOG
from django.core.cache import cache
from  redis import Redis
from datetime import datetime
from cab_services.models import Batch, cab
from user_servcies.models import commuter,Driver
def get_batch_data(pk):
    return Batch.objects.get(pk=pk)

def get_d2d_log_data(batch_id):
    return get_object_or_404(
        DTODLOG,batchId=batch_id
    )

def get_commuter_data(pk):
    commuterData = get_object_or_404(
        commuter.objects.prefetch_related("userId", "popId"), userId=pk
    )
    output = {}
    output[commuterData.userId.id] = {}
    output[commuterData.userId.id]["pickUpPoint"] = commuterData.popId.pickUpPointName
    output[commuterData.userId.id]["mobile_number"] = commuterData.userId.mobileNumber
    output[commuterData.userId.id]["username"] = commuterData.userId.username
    output[commuterData.userId.id]['inLine'] = commuterData.popId.inLine
    return output

def get_set_name(batch_id:str)->str:
    today = datetime.today()
    formatted_date = today.strftime("%d-%m-%Y")
    return formatted_date + '_' + batch_id

def capcaity_check(capacity:int,current_count:int)->int:
    return capacity - current_count

def get_cache_data(batch_id:str)->set:
    redis_object = connect_redis()
    set_name = get_set_name(batch_id)
    cache_data = redis_object.smembers(
        set_name
    )
    return cache_data
    
def add_cache_data(batch_id:str,commuter_id:str)->None:
    redis_object = connect_redis()
    set_name = get_set_name(batch_id)
    redis_object.sadd(set_name,commuter_id)
    close_redis_connection(redis_object)

def connect_redis()->Redis:
    return Redis(
        host='redis',
        port=6379
        )

def close_redis_connection(redis_connection:Redis):
    redis_connection.close()

def turn_off_iscomming(commuter_id:str)->None:
    commuter_data = commuter.objects.get(
                    pk=commuter_id
                )
    commuter_data.isComing = False
    commuter_data.save()

def get_cab_capcity(batch_id:str)->int:
    driver_data:Driver = Driver.objects.get(
                    batchId = batch_id
            )
    cab_data:cab = cab.objects.get(
        pk = driver_data.cabId.id
    )
    return cab_data.capacity

def clear_cache(batch_id:str)->None:
    redis_object = connect_redis()
    set_name = get_set_name(batch_id)
    redis_object.delete(set_name)
    
def remove_cache_data(batch_id:str,commuter_id:str)->None:
    redis_object = connect_redis()
    set_name = get_set_name(batch_id)
    redis_object.srem(set_name,commuter_id)
