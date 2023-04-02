from django.shortcuts import render
from .models import Version
from .models import Schedule23Spring

# Create your views here.
def index(request) :
    version = Version.objects.all()
    schedule = Schedule23Spring.objects.all()
    
    weekday = ['월', '화', '수', '목', '금', '토', '일']
    
    return render(request, 'index.html', {"versions": version, "schedules": schedule, "weekday": weekday})
