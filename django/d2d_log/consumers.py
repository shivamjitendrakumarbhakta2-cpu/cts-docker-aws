import json

# from numpy import dsplit
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from django.core import serializers
import traceback
import channels.layers
import time
from asgiref.sync import sync_to_async

# from .models import DTODLOG
from channels.db import database_sync_to_async
from user_servcies.models import User, commuter
from cab_services.models import pickUpPoints, Batch
from datetime import date
from .models import DTODLOG
from channels.layers import get_channel_layer

# from user_servcies.Serializers import commuterSerializer
import json
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

# from user_servcies.models import commuter

"""
# Get a list of channels in a group
ch_group_list = channel_layer.group_channels('<your group name>')

"""


@database_sync_to_async
def extend_d2d_clist(d2d_log, CList):
    # print(f"D2D_log {d2d_log},ClIST:{d2d_log.CList}")
    print("EXTENDING DATA TO CLIST")
    d2d_log.CList.extend(CList)
    d2d_log.save()
    return d2d_log.CList

@database_sync_to_async
def update_d2d_log_is_active(d2d_log):
    d2d_log.isActive = False
    d2d_log.endTime = now()
    d2d_log.save()
    return True

@database_sync_to_async
def get_d2d_Data(pk):
    return DTODLOG.objects.get(pk=pk)


@database_sync_to_async
def get_user_Data(pk):
    return User.objects.get(pk=pk)


@database_sync_to_async
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
    # print(commuter_serailized_data)

@database_sync_to_async
def get_pop_Data(pk):
    return pickUpPoints.objects.get(pk=pk)


@database_sync_to_async
def get_batch_Data(pk):
    return Batch.objects.get(pk=pk)


@database_sync_to_async
def create_d2d_Data(pk, date):
    dtodlog = DTODLOG.objects.filter(batchId=pk, tripDate=date).first()
    # If the object exists, return its Id
    if dtodlog is not None:
        # Now, Here if True it exsist, That means driver disconnected abnormally
        return True, dtodlog
    # If the object does not exist, create a new one
    else:
        new_dtodlog = DTODLOG.objects.create(batchId=pk)
        return False, new_dtodlog

@database_sync_to_async
def update_d2d_log(d2d_log_data):
    d2d_log_data.isActive = False
    d2d_log_data.save()
    return True

@database_sync_to_async
def update_commuter_is_comming(pk):
    commuter_data = commuter.objects.filter(userId=pk).first()
    commuter_data.isComing = False
    commuter_data.save()
    return True

class d2d(AsyncWebsocketConsumer):
    async def connect(self):
        
        await self.accept()

        batch = self.scope["url_route"]["kwargs"]["batch_id"]
        batch_name = f"{str(date.today())}batch{batch}"
        
        userData = self.scope["user"]
        print("User Data->",userData)

        self.channel_group = batch_name
        batchData = await get_batch_Data(batch)
        logExsists, D2D = await create_d2d_Data(batchData, date.today())
        if logExsists:
            await self.channel_layer.group_add(self.channel_group, self.channel_name)
            self.channel_layer = get_channel_layer()
            print("CHANNEL LAYER->",self.channel_layer)
            DS = getattr(self.channel_layer, batch_name)
            await self.send(text_data=json.dumps({"result": DS}))
        # if getattr(self.channel_layer, batch_name):
        else:
            await self.channel_layer.group_add(self.channel_group, self.channel_name)

            commuter_data = await database_sync_to_async(list)(
                commuter.objects.prefetch_related("userId").filter(
                    batchId=batch, isComing=True
                )
            )

            commuter_serailized_data = json.loads(
                serializers.serialize("json", commuter_data)
            )

            DS = {}
            DS["data"] = []
            # print(f"CLIST->")
            for i in commuter_serailized_data:
                userId = i["fields"]["userId"]
                if not((logExsists) and (userId in D2D.CList)):
                    temp = {}
                    # userId = i["fields"]["userId"]
                    temp[userId] = {}
                    userData = await get_user_Data(pk=userId)
                    popData = await get_pop_Data(pk=i["fields"]["popId"])
                    temp[userId]["pickUpPoint"] = popData.pickUpPointName
                    temp[userId]["inLine"] = popData.inLine
                    temp[userId]["mobile_number"] = userData.mobileNumber
                    temp[userId]["username"] = userData.username
                    DS["data"].append(temp)
                # else:
                #     print(f"OT WORKIN FOR {i}")
                
            DS["D2D_id"] = D2D.id
            setattr(self.channel_layer, batch_name, DS)
            print("CHANNEL LAYER->",self.channel_layer)
            await self.send(text_data=json.dumps({"result": DS}))

    async def disconnect(self, code):
        
        
        await self.channel_layer.group_discard(self.channel_group, self.channel_name)
        
        # batch = self.scope["url_route"]["kwargs"]["batch_id"]
        # batch_name = f"{str(date.today())}batch{batch}"
        # # Get d2d_log id and update isActive to False
        # # Get The CList and set isComming to false for each commuter
        # if not(isinstance(code, int)):
        #     if json.loads(code)['CODE'] == 100:
                
        #     else:
        #         print("NOT CALLED")
        #         return await self.close()


    async def receive(self, text_data):
        # retrive Data Based on ASC inLine
        print("EVENT CALLED")
        batch = self.scope["url_route"]["kwargs"]["batch_id"]
        batch_name = f"{str(date.today())}batch{batch}"
        userData = self.scope["user"]
        if text_data is not None:
            
            input_data = json.loads(text_data)

        DS = getattr(self.channel_layer, batch_name)
        
        if input_data["ACTION"] == "REMOVE":  # add data to d2d Log
            d2d_log = await get_d2d_Data(DS["D2D_id"])  # type: ignore

        
            Clist = []
            for i in DS["data"]:
        
                if list(i.keys())[0] in input_data["CLIST"] and list(i.keys())[0] not in d2d_log.CList:
                    Clist.append(list(i.keys())[0])
            
            updatedList = await extend_d2d_clist(d2d_log, Clist)
            DS["data"] = [d for d in DS["data"] if list(d.keys())[0] not in Clist]
            
        elif input_data["ACTION"] == "ADD": # Add Data to DS
            Clist = []
            d2d_log = await get_d2d_Data(DS["D2D_id"])
            
            if input_data['CLIST'] not in d2d_log.CList and not(any(input_data['CLIST'] in d for d in DS['data'])):
            
                new_record = await get_commuter_data(input_data["CLIST"])   
                DS["data"].append(new_record)
            
        elif input_data['ACTION'] =="DELETE": # Remove from DS
            DS['data'] = [d for d in DS['data'] if list(d.keys())[0] not in input_data["CLIST"]]
        
        elif input_data['ACTION'] == 'STOP':
            DS = getattr(self.channel_layer, batch_name)
                # d2d_log_id = DS['D2D_id']
        
            userData = self.scope["user"]
            d2d_log = await get_d2d_Data(DS["D2D_id"])

            #TODO: if message -> DELETE
            await update_d2d_log_is_active(d2d_log)
    
            for commuter_id in d2d_log.CList:
                await update_commuter_is_comming(commuter_id)
            delattr(self.channel_layer, batch_name)  # if userType == Driver and code == 100

            # commuter_list = list(d for d in DS['data'] )
            
            # Deleting the attribute

            
            return await self.disconnect(0)
            
        setattr(self.channel_layer, batch_name, DS)
        await self.channel_layer.group_send(
            self.channel_group, {"type": "notification_message", "message": DS}
        )

    async def notification_message(self, event):
        print("EVENT MESSAGE CALLED")
        message = event["message"]
        await self.send(text_data=json.dumps({"result": message}))


# class d2d(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         print("Connected")
#         # self.expressions = {}
#         batch = self.scope["url_route"]["kwargs"]["temp"]
#         batch_name = f"{str(date.today())}batch{batch}"
#         self.channel_group = batch_name
#         print(f"user->{self.scope['user']}")
#         print(f"scope-{self.scope}")
#         self.user = self.scope["user"]
#         setattr(self.channel_layer, batch_name, {"BATCHNAME": batch_name})
#         print(
#             "GET ATTRIBUTE", getattr(self.channel_layer, batch_name)
#         )  ### PROGRESSSS AS OF 27-10-23
#         # TODO
#         """
#         # if self.user.userType == 'DRIVER':
#         ## In this case Create DS
#         # elif self.user.userType == 'ADMIN':
#         ## In this case, check if group exists if do return self.DS
#         ## if hasattr(self.channel_layer, self.group_name):
#         """
#         # self.channel_layer['f"{str(date.today())}batch{batch}"']
#         batchData = await get_batch_Data(batch)
#         logExsists, D2D = await create_d2d_Data(batchData, date.today())
#         # self.channel_layer.data[f"{str(date.today())}batch{batch}"] = {}
#         # print(self.channel_layer.data)
#         # if self.user.userType == "ADMIN"
#         # print()
#         if logExsists:
#             print("EXSITS")
#             await self.channel_layer.group_add(self.channel_group, self.channel_name)
#             DS = getattr(self.channel_layer, batch_name)

#             await self.send(text_data=json.dumps({"result": self.channel_layer.DS}))
#             # await self.send(text_data=json.dumps({"result": self.channel_layer.DS}))
#         else:
#             commuter_data = await database_sync_to_async(list)(
#                 commuter.objects.prefetch_related("userId").filter(
#                     batchId=batch, isComing=True
#                 )
#             )
#             commuter_serailized_data = json.loads(
#                 serializers.serialize("json", commuter_data)
#             )
#             # self.DS  = { "data": []}

#             self.channel_layer.DS = {"data": []}
#             # print(self.cha)
#             for i in commuter_serailized_data:
#                 temp = {}
#                 temp[i["pk"]] = {}
#                 userId = i["fields"]["userId"]
#                 userData = await get_user_Data(pk=userId)
#                 popData = await get_pop_Data(pk=i["fields"]["popId"])
#                 temp[i["pk"]]["pickUpPoint"] = popData.pickUpPointName
#                 temp[i["pk"]]["mobile_number"] = userData.mobileNumber
#                 temp[i["pk"]]["first_name"] = userData.first_name
#                 self.channel_layer.DS["data"].append(temp)

#             self.channel_layer.D2D_id = D2D.id
#             # print("D2D_id",D2D.id)
#             # print(len(commuter_serailized_data))
#             # print(result)
#             # print(self.channel_name)
#             # print(self.channel_layer)
#             # print(self.channel_group)
#             await self.channel_layer.group_add(self.channel_group, self.channel_name)

#             await self.send(text_data=json.dumps({"result": "self.channel_layer.DS"}))

#     async def disconnect(self, close_code):
#         print(self.scope["url_route"]["kwargs"]["temp"])
#         try:
#             print("CLOSE CODE->", close_code)
#             if close_code != 1000:
#                 cahche_data = cache.get(
#                     str(self.scope["url_route"]["kwargs"]["temp"]) + "+D2D"
#                 )
#                 if cahche_data:
#                     cahche_data.append(
#                         self.expressions[self.scope["url_route"]["kwargs"]["temp"]]
#                     )
#                 else:
#                     cahche_data = self.expressions[
#                         self.scope["url_route"]["kwargs"]["temp"]
#                     ]
#                 cache.set(
#                     str(self.scope["url_route"]["kwargs"]["temp"]) + "+D2D", cahche_data
#                 )
#                 print("data cached")
#                 await self.close()
#             else:
#                 print("NORAML disconnection")
#                 await self.channel_layer.group_discard(
#                     self.channel_group, self.channel_name
#                 )
#         except Exception as e:
#             print(traceback.print_exc())

#     async def receive(self, text_data):
#         print(self.scope["url_route"]["kwargs"]["temp"])
#         # print("DS For you is:", self.channel_layer.DS)
#         # channel_layer = channels.layers.get_channel_layer()
#         print("IN RECEIVE")
#         # print(json.loads(text_data))
#         input_data = json.loads(text_data)
#         # print("YOURE ARE WORKING FOR,",self.D2D_id)
#         # print(self.channel_layer)
#         # print(self.channel_name)

#         """
#         # TODO
#         # Here Check userType
#             # if DRIVER -> ADD_D2D
#             # elif ADMIN -> ADD_DS
#         """
#         print(self.channel_layer.DS)
#         print(self.scope["user"])
#         # if self.scope['user'].userType == 'DRIVER'
#         if input_data["ACTION"] == "ADD":
#             print(type(input_data["CLIST"]))
#             d2d_log = await get_d2d_Data(self.channel_layer.D2D_id)  # type: ignore
#             Clist = []
#             for i in self.channel_layer.DS["data"]:
#                 # print(i,type(i))
#                 if list(i.keys())[0] in input_data["CLIST"]:
#                     Clist.append(list(i.keys())[0])

#             updatedList = await extend_d2d_clist(d2d_log, Clist)
#             # temp = self.DS

#             self.channel_layer.DS["data"] = [
#                 d for d in self.DS["data"] if list(d.keys())[0] not in Clist
#             ]
#         message = self.channel_layer.DS
#         await self.channel_layer.group_send(
#             self.channel_group, {"type": "notification_message", "message": message}
#         )

#     async def notification_message(self, event):
#         print("EVENT MESSAGE CALLED")
#         message = event["message"]
#         print(event)
#         print("in_chat")
#         await self.send(text_data=json.dumps({"result": message}))