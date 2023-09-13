from __future__ import absolute_import

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from cab_services.models import Batch, cab, pickUpPoints

import uuid


class User(AbstractUser):
    userType = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=False, null=True)
    mobileNumber = models.CharField(max_length=20, unique=True, null=False)
    USERNAME_FIELD = "mobileNumber"


class subAdmin(models.Model):
    userId = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False
    )
    address = models.CharField(max_length=100, null=True)
    id = models.CharField(
        primary_key=True, default=str(uuid.uuid4())[:4], editable=False, max_length=4
    )


class commuter(models.Model):
    collegeName = models.CharField(max_length=100, null=True)
    cabId = models.ForeignKey(cab, on_delete=models.SET_NULL, null=True)
    popId = models.ForeignKey(pickUpPoints, on_delete=models.SET_NULL, null=True)
    isComing = models.BooleanField(default=True, null=False)
    userId = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False
    )
    batchId = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    adminCode = models.ForeignKey(subAdmin, on_delete=models.SET_NULL, null=True)


class Driver(models.Model):
    userId = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False
    )
    address = models.CharField(max_length=100, null=True)
    adminCode = models.ForeignKey(subAdmin, on_delete=models.SET_NULL, null=True)
    batchId = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True)
    cabId = models.ForeignKey(cab, on_delete=models.SET_NULL, null=True)
