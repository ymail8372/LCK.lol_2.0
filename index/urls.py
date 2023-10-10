from django.urls import path
from . import views

urlpatterns = [
    path('get_schedules_Json', views.get_schedules_Json),
    path('get_champions_Json', views.get_champions_Json),
    path('', views.index),
	path('schedule', views.schedule),
]
