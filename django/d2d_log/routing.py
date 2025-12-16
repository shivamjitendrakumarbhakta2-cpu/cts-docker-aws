from django.urls import re_path
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path("ws/<int:batch_id>/", consumers.d2d.as_asgi()),
]
