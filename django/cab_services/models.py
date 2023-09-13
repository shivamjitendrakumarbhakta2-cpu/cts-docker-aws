# from __future__ import absolute_import

from django.db import models

# from django.contrib.auth.models import User
from django.conf import settings

# from user_servcies.models import admin
from django.apps import apps


# Create your models here.
class Routes(models.Model):
    routeName = models.CharField(max_length=100)
    adminCode = models.ForeignKey(
        "user_servcies.subAdmin", on_delete=models.SET_NULL, null=True
    )


class Batch(models.Model):
    batchName = models.CharField(max_length=100)
    batchTime = models.TimeField(auto_now=False, auto_now_add=False, null=True)
    endDate = models.DateField(null=True)  # type: ignore
    startDate = models.DateField(null=True)  # type: ignore
    adminCode = models.ForeignKey(
        "user_servcies.subAdmin", on_delete=models.SET_NULL, null=True
    )


class pickUpPoints(models.Model):
    pickUpPointName = models.CharField(max_length=100)
    lat = models.FloatField()
    longitude = models.FloatField()
    routeId = models.ForeignKey(Routes, on_delete=models.SET_NULL, null=True)
    adminCode = models.ForeignKey(
        "user_servcies.subAdmin", on_delete=models.SET_NULL, null=True
    )


class cab(models.Model):
    regNumber = models.CharField(max_length=100, null=True,unique=True)
    capacity = models.IntegerField()
    adminCode = models.ForeignKey("user_servcies.subAdmin", on_delete=models.SET_NULL, null=True)  # type: ignore
    km = models.IntegerField()
    regDate = models.DateTimeField(auto_now_add=True)
    routeId = models.ForeignKey(Routes, on_delete=models.SET_NULL, null=True)
    thumbnail = models.BinaryField(null=True)
