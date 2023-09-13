from django.urls import path
from . import views


app_name  = 'cab_services'

urlpatterns = [
    path("route",views.route.as_view()),
    path("route/<int:pk>",views.routes.as_view()),
    path("batch",views.batch.as_view()),
    path("batch/<int:pk>",views.batchs.as_view()),
    path("pickUpPoint",views.pick_up_point.as_view()),
    path("pickUpPoint/<int:pk>",views.pick_up_points.as_view()),
    path("cab",views.Cab.as_view()),
    path("cab/<int:pk>",views.Cabs.as_view()),
    path("admin/<str:name>/<str:pk>",views.custom_admin.as_view())
]