from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('get_schedules_Json', views.get_schedules_Json),
    path('get_champions_Json', views.get_champions_Json),
]
