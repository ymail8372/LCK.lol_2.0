from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_schedules', views.get_schedules, name="get_schedules"),
]