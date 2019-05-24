from django.urls import path

from ws import consumers

websocket_urlpatterns = [
    path('ws/core/', consumers.CoreConsumer),
    path('ws/store/', consumers.StoreConsumer),
    path('ws/sensor/', consumers.SensorConsumer),
]