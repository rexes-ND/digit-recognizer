from django.urls import path

from . import views

urlpatterns = [
    path("recognize/", views.RecognizeAPIView.as_view()),
]
