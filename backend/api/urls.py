from django.urls import path

from . import views

urlpatterns = [
    path("recognize/", views.recognize),
]
