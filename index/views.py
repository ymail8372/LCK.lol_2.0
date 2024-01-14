from django.shortcuts import render

from index import models
from index.models import Schedule
from index.models import Ranking_24_spring_regular
from django.http import HttpResponse

def champion_table(request) :
	league = request.GET.get('league', '')
	patch = request.GET.get('patch', '')
	sort = request.GET.get('sort', '')

	champions = get_champions(league, patch, sort)
	
	if champions == "no_model" :
		return HttpResponse("<script>alert(\"Error!\"); window.location.href = \"/champion?league=LCK_summer&patch=13.14\";</script>")
	
	return render(request, "champion_table.html", {"champions": champions})

def get_champions(league, patch,  sort='') :
	champions = []
	
	champion_model = getattr(models, f"Champion_23_{league}", "no_model")
	
	if champion_model == "no_model" :
		#print("no_model_league")
		return "no_model"
	
	# patch != all
	if patch != "all" :
		champion_objects = champion_model.objects.filter(patch = patch)
		if len(champion_objects) == 0 :
			#print("no_model_patch")
			return "no_model"
		
		for champion_object in champion_objects :
			new_champion = {}
			new_champion['name'] = champion_object.name
			new_champion['pick'] = champion_object.pick
			new_champion['ban'] = champion_object.ban
			new_champion['win'] = champion_object.win
			new_champion['lose'] = champion_object.lose
			new_champion['patch'] = champion_object.patch
			
			champions.append(new_champion)
		
	# patch == all
	else :
		champion_objects = champion_model.objects.all()
		if len(champion_objects) == 0 :
			print("no_model_patch")
			return "no_model"
		
		for champion_object in champion_objects :
			champion_already_in_champion_all = 0
			# check whether the champion is in already in champions_all
			for champion_all in champions :
				if champion_all['name'] == champion_object.name :
					champion_already_in_champion_all = 1
					
					champion_all['pick'] += champion_object.pick
					champion_all['ban'] += champion_object.ban
					champion_all['win'] += champion_object.win
					champion_all['lose'] += champion_object.lose
					break
				
			if champion_already_in_champion_all == 0 :
				champions.append({"name": champion_object.name, "pick": champion_object.pick, "ban": champion_object.ban, "win": champion_object.win, "lose": champion_object.lose, "patch": "all"})
	
	# calculate banpick_rate, win_rate
	total_game = 0
	for champion in champions :
		total_game += champion['pick']
	total_game = total_game / 10
	
	for champion in champions :
		if total_game != 0 :
			champion["banpick_rate"] = round((champion["pick"] + champion["ban"]) / total_game * 100, 1)
		else :
			champion["banpick_rate"] = 0.0
		
		if champion["pick"] != 0 :
			champion["win_rate"] = round(champion["win"] / champion["pick"] * 100, 1)
		else :
			champion["win_rate"] = 0.0
	
	if sort == "" :
		print("banpick_rate")
		champions = sorted(champions, key=lambda x: x["banpick_rate"], reverse=True)
	elif "pick_menu" in sort :
		if "descending" in sort :
			champions = sorted(champions, key=lambda x: x["pick"], reverse=True)
		else :
			champions = sorted(champions, key=lambda x: x["pick"])
	elif "ban_menu" in sort :
		if "descending" in sort :
			champions = sorted(champions, key=lambda x: x["ban"], reverse=True)
		else :
			champions = sorted(champions, key=lambda x: x["ban"])
	elif "banpick_rate_menu" in sort :
		if "descending" in sort :
			champions = sorted(champions, key=lambda x: x["banpick_rate"], reverse=True)
		else :
			champions = sorted(champions, key=lambda x: x["banpick_rate"])
	elif "win_menu" in sort :
		if "descending" in sort :
			champions = sorted(champions, key=lambda x: x["win"], reverse=True)
		else :
			champions = sorted(champions, key=lambda x: x["win"])
	elif "lose_menu" in sort :
		if "descending" in sort :
			champions = sorted(champions, key=lambda x: x["lose"], reverse=True)
		else :
			champions = sorted(champions, key=lambda x: x["lose"])
	elif "win_rate_menu" in sort :
		if "descending" in sort :
			champions = sorted(champions, key=lambda x: x["win_rate"], reverse=True)
		else :
			champions = sorted(champions, key=lambda x: x["win_rate"])
	
	
	return champions

def index(request) :
	# champions
	champions = get_champions('LCK_summer', 'all')
	champions_all = []
	
	# champions (patch == all)
	for champion in champions :
		if champion["patch"] == "all" :
			champions_all.append(champion)
	
	# schedules
	schedules = Schedule.objects.all()
	
	# ranking
	ranking_24_spring_regular = Ranking_24_spring_regular.objects.all()
	
	# make ranking dictionary
	ranking_list = []
	for ranking in ranking_24_spring_regular :
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
	
	
	return render(request, 'index.html', {"schedules": schedules, "champions": champions_all[0:5], "ranking_list": ranking_list})

def schedule(request) :
	# schedules
	schedules = Schedule.objects.all().order_by("month", "day", "hour")
	
	# schedules (year == 2023)
	schedules_2024 = []
	for schedule in schedules :
		if schedule.year == '2024' :
			schedules_2024.append(schedule)

	# teams
	teams_2024_1 = ['BRO', 'DK', 'DRX', 'GEN', 'HLE', 'KDF', 'KT', 'FOX', 'NS', 'T1']

	return render(request, 'schedule.html', {"schedules": schedules_2024, "teams_2024_1": teams_2024_1})

def ranking(request) :
	# ranking
	ranking_24_spring_regular = Ranking_24_spring_regular.objects.all()
	
	# make ranking dictionary
	ranking_list = []
	for ranking in ranking_24_spring_regular :
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
	
	return render(request, "champion.html")

def history(request) :
	year = request.GET.get("year", "")
	league = request.GET.get("league", "")
	
	return render(request, f"history_contents/{league}/{year}.html")
