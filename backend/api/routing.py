from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path("ws/scoring/", consumers.ScoringConsumer.as_asgi()),
]
