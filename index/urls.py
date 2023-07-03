from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('get_schedules', views.get_schedules),
]