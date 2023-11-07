from django.shortcuts import render
from .models import Schedule
from .models import Champion_23_summer
from .models import Ranking_23_summer_regular
from django.http import HttpResponse

# get champions for patch == all
def get_champions(league, patch) :
	champions = []
	
	if league == "LCK_spring" :
		pass
	elif league == "MSI" :
		pass
	elif league == "LCK_summer" :
		pass
	else :
		pass
	
	champion_objects = Champion_23_summer.objects.all()
	for champion_object in champion_objects :
		new_champion = {}
		new_champion['name'] = champion_object.name
		new_champion['pick'] = champion_object.pick
		new_champion['ban'] = champion_object.ban
		new_champion['win'] = champion_object.win
		new_champion['lose'] = champion_object.lose
		new_champion['patch'] = champion_object.patch
		
		champions.append(new_champion)
	
	# all patch champions
	champions_all_patch = []
	
	for champion in champions :
		champion_already_in_champion_all = 0
		# check whether the champion is in already in champions_all
		for champion_all in champions_all_patch :
			if champion_all['name'] == champion['name'] :
				champion_already_in_champion_all = 1
				
				champion_all['pick'] += champion['pick']
				champion_all['ban'] += champion['ban']
				champion_all['win'] += champion['win']
				champion_all['lose'] += champion['lose']
				break
			
		if champion_already_in_champion_all == 0 :
			champions_all_patch.append({"name": champion["name"], "pick": champion["pick"], "ban": champion["ban"], "win": champion["win"], "lose": champion["lose"], "patch": "all"})
	
	champions.extend(champions_all_patch)
	
	total_game = 0
	for champion_all_patch in champions_all_patch :
		total_game += champion_all_patch['pick']
	total_game = total_game / 10
	
	for champion in champions :
		if total_game != 0 :
			champion["banpick_rate"] = round((champion["pick"] + champion["ban"]) / total_game * 100, 1)
		else :
			champion["banpick_rate"] = 0
		
		if champion["pick"] != 0 :
			champion["win_rate"] = round(champion["win"] / champion["pick"] * 100, 1)
		else :
			champion["win_rate"] = 0
		
	champions = sorted(champions, key=lambda x: x["banpick_rate"], reverse=True)
	
	#for champion in champions :
	#	print(champion['name'], champion['pick'])
	
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
	schedules = Schedule.objects.all().order_by("month", "day", "hour")
	
	# schedules (year == 2023)
	schedules_2023 = []
	for schedule in schedules :
		if schedule.year == '2023' :
			schedules_2023.append(schedule)

	# teams
	teams_2023_3 = ['BRO', 'DK', 'DRX', 'GEN', 'HLE', 'KDF', 'KT', 'LSB', 'NS', 'T1']
	teams_2023_10 = ["GEN", "T1", "KT", "DK"]

	return render(request, 'schedule.html', {"schedules": schedules_2023, "teams_2023_3": teams_2023_3, "teams_2023_10": teams_2023_10})

def ranking(request) :
	# ranking
	ranking_23_summer_regular = Ranking_23_summer_regular.objects.all()
	
	# make ranking dictionary
	ranking_list = []
	for ranking in ranking_23_summer_regular :
		new_ranking = {}
		new_ranking["team"] = ranking.name
		new_ranking["tricode"] = ranking.tricode
		new_ranking["game_win"] = ranking.game_win
		new_ranking["game_lose"] = ranking.game_lose
		new_ranking["set_win"] = ranking.set_win
		new_ranking["set_lose"] = ranking.set_lose
		new_ranking["set_diff"] = ranking.set_win - ranking.set_lose
		new_ranking["etc"] = ranking.etc
		ranking_list.append(new_ranking)
	
	ranking_list.sort(key = lambda ranking: (ranking["game_win"], ranking["set_diff"]), reverse=True)
	
	for i in range(len(ranking_list)) :
		if i == 0 :
			ranking_list[i]["ranking"] = 1
		else :
			if ranking_list[i]["game_win"] == ranking_list[i-1]["game_win"] and ranking_list[i]["set_diff"] == ranking_list[i-1]["set_diff"] :
				ranking_list[i]["ranking"] = ranking_list[i-1]["ranking"]
			else :
				ranking_list[i]["ranking"] = i+1
	
	return render(request, 'ranking.html', {"ranking_list": ranking_list})

def champion(request) :
	league = request.GET.get('league')
	patch = request.GET.get('patch')
	
	if (league != "LCK_spring" and league != "MSI" and league != "LCK_summer" and league != "Worlds") :
		return HttpResponse("<script>alert(\"Error!\"); window.history.back();</script>")
	
	champions = get_champions(league, patch)
	
	return render(request, "champion.html", {"champions": champions})
