from django.shortcuts import render
from django.http import JsonResponse
from .models import Schedule
from .models import Champion

# response Json to JS
def get_schedules_Json(request) :
    schedule_values = Schedule.objects.values()
    
    return JsonResponse(list(schedule_values), safe=False)

def get_champions_Json(request) :
    champion_values = get_champions()
    
    return JsonResponse(champion_values, safe=False)

# get champions for patch == all
def get_champions() :
    champions = []
    
    champion_objects = Champion.objects.all()
    for champion_object in champion_objects :
        new_champion = {}
        new_champion['name'] = champion_object.name
        new_champion['pick'] = champion_object.pick
        new_champion['ban'] = champion_object.ban
        new_champion['win'] = champion_object.win
        new_champion['lose'] = champion_object.lose
        new_champion['patch'] = champion_object.patch
        
        champions.append(new_champion)
    
    champions_all = []
    
    for champion in champions :
        champion_in_champion_all = 0
        for champion_all in champions_all :
            if champion_all['name'] == champion['name'] :
                champion_in_champion_all = 1
                
                champion_all['pick'] += champion['pick']
                champion_all['ban'] += champion['ban']
                champion_all['win'] += champion['win']
                champion_all['lose'] += champion['lose']
                break
            
        if champion_in_champion_all == 0 :
            champions_all.append({"name": champion["name"], "pick": champion["pick"], "ban": champion["ban"], "win": champion["win"], "lose": champion["lose"], "patch": "all"})
            
    champions.extend(champions_all)
    
    total_game_13_10 = 0
    total_game_13_11 = 0
    total_game_13_12 = 0
    
    for i in range(len(champions)) :
        if champions[i]["patch"] == "13.10" :
            total_game_13_10 += champions[i]["pick"]
        elif champions[i]["patch"] == "13.11" :
            total_game_13_11 += champions[i]["pick"]
        elif champions[i]["patch"] == "13.12" :
            total_game_13_12 += champions[i]["pick"]
    
    total_game_13_10 /= 10
    total_game_13_11 /= 10
    total_game_13_12 /= 10
    total_game = total_game_13_10 + total_game_13_11 + total_game_13_12
    
    for i in range(len(champions)) :
        if total_game != 0 :
            champions[i]["banpick_rate"] = round((champions[i]["pick"] + champions[i]["ban"]) / total_game * 100, 1)
        else :
            champions[i]["banpick_rate"] = 0
        
        if champions[i]["pick"] != 0 :
            champions[i]["win_rate"] = round(champions[i]["win"] / champions[i]["pick"] * 100, 1)
        else :
            champions[i]["win_rate"] = 0
        
    champions = sorted(champions, key=lambda x: x["banpick_rate"], reverse=True)
    
    return champions

def index(request) :
    # champions
    champions = get_champions()
    champions_all = []
    
    # champions (patch == all)
    for champion in champions :
        if champion["patch"] == "all" :
            champions_all.append(champion)
    
    # schedules
    schedules = Schedule.objects.all()
    
    return render(request, 'index.html', {"schedules": schedules, "champions": champions_all[0:5]})

def schedule(request) :
    # schedules
    schedules = Schedule.objects.all()
    
    # schedules (year == 2023)
    schedules_2023 = []
    for schedule in schedules :
        if schedule.year == '2023' :
            schedules_2023.append(schedule)
    
    # teams
    teams_2023 = ['BRO', 'DK', 'DRX', 'GEN', 'HLE', 'KDF', 'KT', 'LSB', 'NS', 'T1']
    
    return render(request, 'schedule.html', {"schedules": schedules_2023, "teams": teams_2023})
