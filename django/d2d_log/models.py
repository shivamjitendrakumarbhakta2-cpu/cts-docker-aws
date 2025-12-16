from django.db import models
from django.contrib.postgres.fields import ArrayField
# from cab_services.models import Batch
from django.utils import timezone
# Create your models here.
class DTODLOG(models.Model):

    CList = ArrayField(models.IntegerField(), default=list)
    batchId = models.ForeignKey("cab_services.Batch", on_delete=models.SET_NULL, null=True)
    
    startTime = models.DateTimeField(auto_now_add=True)
    endTime = models.DateTimeField(null=True, blank=True)
    return_start_time = models.TimeField(null=True, blank=True)
    return_end_time = models.TimeField(null=True, blank=True)
    tripDate = models.DateField(default=timezone.now)
    isActive = models.BooleanField(default=True,null=True)
    
