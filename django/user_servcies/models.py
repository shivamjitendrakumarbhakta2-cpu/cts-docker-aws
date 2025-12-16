from __future__ import absolute_import

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from cab_services.models import Batch, cab, pickUpPoints

import uuid


class User(AbstractUser):
    userType = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=False, null=True)
    mobileNumber = models.CharField(max_length=10, unique=True, null=False)
    address = models.CharField(max_length=100, null=True)
    USERNAME_FIELD = "mobileNumber"
    deviceId = models.CharField(max_length=100, unique=False, null=True)
    hasPaid = models.BooleanField(default=False,null=True)



class subAdmin(models.Model):
    userId = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    
class commuter(models.Model):
    collegeName = models.CharField(max_length=100, null=True)
    cabId = models.ForeignKey(cab, on_delete=models.SET_NULL, null=True)
    popId = models.ForeignKey(pickUpPoints, on_delete=models.SET_NULL, null=True)
    isComing = models.BooleanField(default=True, null=False)
    userId = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False
    )
    batchId = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)
    adminCode = models.ForeignKey(subAdmin, on_delete=models.SET_NULL, null=True)


class Driver(models.Model):
    userId = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False
    )
    adminCode = models.ForeignKey(subAdmin, on_delete=models.SET_NULL, null=True)
    batchId = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)
    cabId = models.ForeignKey(cab, on_delete=models.SET_NULL, null=True)
    class Meta:
        unique_together = [['batchId', 'cabId']]

        