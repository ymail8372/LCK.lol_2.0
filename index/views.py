from django.shortcuts import render
from .models import Version
from .models import Schedule

# Create your views here.
def index(request) :
    version = Version.objects.all()
    schedule = Schedule.objects.all()
    
    print(type(schedule[0].date))
    
    return render(request, 'index.html', {"versions": version, "schedules": schedule})
