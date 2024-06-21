from django.urls import path
from . import views

urlpatterns = [
    #path('get_schedules_Json', views.get_schedules_Json),
    #path('get_champions_Json', views.get_champions_Json),
    path('', views.index),
	path('schedule', views.schedule),
	path('ranking', views.ranking),
	path('champion', views.champion),
	path('champion_table', views.champion_table),
	path('history', views.history),
	path('ads.txt', views.Ads),
	path('navered740bad61f2dffe423226b77ebdff35.html', views.naver)
]
