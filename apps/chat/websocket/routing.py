from .consumers import ChatConsumer
from django.urls import path

websocket_urlpatterns = [
    path('chat/<int:ticket_id>/',ChatConsumer.as_asgi())
]