from django.shortcuts import render
from django.http import JsonResponse
from .models import Schedule

# response Json to JS
def get_schedules(request) :
    schedule_values = Schedule.objects.values()
    
    return JsonResponse(list(schedule_values), safe=False)

def index(request) :
    schedules = Schedule.objects.all()
    
    return render(request, 'index.html', {"schedules": schedules})
