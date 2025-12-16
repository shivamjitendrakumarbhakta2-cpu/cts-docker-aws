from django.urls import path
from . import views
app_name  = 'd2d_log'

urlpatterns = [
    path("running_batches/<str:admin_code>",views.RunningBatches.as_view()),
    path("return_batch/view/<str:batch_id>",views.ReturnTrip.as_view()),
    path("return_batch/get_commuter/<str:batch_id>",views.CacheData.as_view()),
    path("return_batch/add_commuter",views.AddCommuter.as_view()),
    path("return_batch/remove_commuter",views.RemoveCacheData.as_view()), 
    path('return_batch/end/<str:batch_id>',views.CleareCacheData.as_view()),
    path("get_d2d_log_status/<str:batch_id>",views.CheckD2dLogStatus.as_view())
]