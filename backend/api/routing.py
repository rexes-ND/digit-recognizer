from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path(
        "ws/digit-recognize/<uuid:task_id>/",
        consumers.DigitRecognizeConsumer.as_asgi(),
    ),
]
