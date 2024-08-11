from django.shortcuts import render

from index import models
from index.models import Schedule
from index.models import Version
from django.http import HttpResponse

from datetime import datetime

# version
version = Version.objects.all()[0]

league_version = version.league_version
live_version = version.live_version
league = "LCK 2024 Summer"

def index(request) :
	# champions
	champions = get_champions(league.split(" ")[1], league.split(" ")[0] + " " + league.split(" ")[2], 'all')
	
	# schedules
	schedules = Schedule.objects.filter(date__gt=datetime(2024, 1, 1))
	
	# ranking
	rankings = getattr(models, f"Ranking_{league.replace(' ', '_')}").objects.all()
	
	# make ranking dictionary
	ranking_list = []
	for ranking in rankings :
		new_ranking = {}
		new_ranking["tournament"] = league
		new_ranking["team"] = ranking.name
		new_ranking["tricode"] = ranking.tricode
		new_ranking["match_win"] = ranking.match_win
		new_ranking["match_lose"] = ranking.match_lose
		new_ranking["set_win"] = ranking.set_win
		new_ranking["set_lose"] = ranking.set_lose
		new_ranking["set_diff"] = ranking.set_win - ranking.set_lose
		new_ranking["etc"] = ranking.etc
		ranking_list.append(new_ranking)
	
	ranking_list.sort(key = lambda ranking: (ranking["match_win"], ranking["set_diff"]), reverse=True)
	
	# set place
	for i in range(len(ranking_list)) :
		if i == 0 :
			ranking_list[i]["ranking"] = 1
		else :
			if ranking_list[i]["match_win"] == ranking_list[i-1]["match_win"] and ranking_list[i]["set_diff"] == ranking_list[i-1]["set_diff"] :
				ranking_list[i]["ranking"] = ranking_list[i-1]["ranking"]
			else :
				ranking_list[i]["ranking"] = i+1
	
	if champions == "Error" :
		return render(request, 'index.html', {"league_version":league_version, "live_version":live_version, "schedules": schedules, "champions": "", "ranking_list": ranking_list})
	else :
		return render(request, 'index.html', {"league_version":league_version, "live_version":live_version, "schedules": schedules, "champions": champions[0:5], "ranking_list": ranking_list})

def get_champions(year, league, patch, sort='') :
	champions = []
	model_name = ""
	
	if "LCK" in league :
		model_name = f"Champion_LCK_{year}_{league.split(' ')[1]}"
	else :
		model_name = f"Champion_{league}_{year}"
	
	champion_model = getattr(models, model_name, "No_champion_DB_model")
	
	if champion_model == "No_champion_DB_model" :
		print("No_champion_DB_model")
		return "Error"
	
	# patch == all
	if patch == "all" :
		champion_objects = champion_model.objects.all()
		if len(champion_objects) == 0 :
			print("no champion at all")
			return "Error"
		
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
	
	# patch == none
	elif patch == "none" :
		champion_objects = champion_model.objects.all()
		if len(champion_objects) == 0 :
			print("no champion at all")
			return "Error"
		
		return champion_objects
		
	# patch == XX.X
	else :
		champion_objects = champion_model.objects.filter(patch = patch)
		#if len(champion_objects) == 0 :
		#	print("no champion at the patch")
		#	return "Error"
		
		for champion_object in champion_objects :
			new_champion = {}
			new_champion['name'] = champion_object.name
			new_champion['pick'] = champion_object.pick
			new_champion['ban'] = champion_object.ban
			new_champion['win'] = champion_object.win
			new_champion['lose'] = champion_object.lose
			new_champion['patch'] = champion_object.patch
			
			champions.append(new_champion)
		
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

def schedule(request) :
	# schedules
	schedules = Schedule.objects.all().order_by("date")
	
	# team tricode list
	teams_2024_1 = set()
	teams_2024_2 = set()
	teams_2024_3 = set()
	
	# schedules (year == 2024)
	schedules_2024 = []
	for schedule in schedules :
		if schedule.date > datetime(2024, 1, 1) :
			if "Spring" in schedule.tournament :
				teams_2024_1.add(schedule.team1_tricode)
				teams_2024_1.add(schedule.team2_tricode)
			elif "MSI" in schedule.tournament :
				teams_2024_2.add(schedule.team1_tricode)
				teams_2024_2.add(schedule.team2_tricode)
			elif "Summer" in schedule.tournament :
				teams_2024_3.add(schedule.team1_tricode)
				teams_2024_3.add(schedule.team2_tricode)
			
			schedules_2024.append(schedule)
	
	if "TBD" in teams_2024_1 :
		teams_2024_1.remove("TBD")
	if "TBD" in teams_2024_2 :
		teams_2024_2.remove("TBD")
	if "TBD" in teams_2024_3 :
		teams_2024_3.remove("TBD")

	return render(request, 'schedule.html', {"schedules": schedules_2024, "teams_2024_1": teams_2024_1, "teams_2024_2": teams_2024_2, "teams_2024_3": teams_2024_3})

def schedule_block(request) :
	date = datetime(int(request.GET.get('year', '')), int(request.GET.get('month', '')), int(request.GET.get('date', '')))
	
	schedule_model = getattr(models, "Schedule", "No_champion_DB_model")
	
	schedules = schedule_model.objects.filter(date__year = str(date.year), date__month = str(date.month), date__day = str(date.day))
	
	return render(request, 'schedule_block.html', {"date": date, "schedules": schedules})

def ranking(request) :
	# team ranking
	rankings_team = getattr(models, f"Ranking_{league.replace(' ', '_')}").objects.all()
	
	ranking_list_team = []
	for ranking_team in rankings_team :
		new_ranking = {}
		new_ranking["team"] = ranking_team.name
		new_ranking["tricode"] = ranking_team.tricode
		new_ranking["match_win"] = ranking_team.match_win
		new_ranking["match_lose"] = ranking_team.match_lose
		new_ranking["set_win"] = ranking_team.set_win
		new_ranking["set_lose"] = ranking_team.set_lose
		new_ranking["set_diff"] = ranking_team.set_win - ranking_team.set_lose
		new_ranking["etc"] = ranking_team.etc
		ranking_list_team.append(new_ranking)
	
	ranking_list_team.sort(key = lambda ranking: (ranking["match_win"], ranking["set_diff"]), reverse=True)
	
	for i in range(len(ranking_list_team)) :
		if i == 0 :
			ranking_list_team[i]["ranking"] = 1
		else :
			if ranking_list_team[i]["match_win"] == ranking_list_team[i-1]["match_win"] and ranking_list_team[i]["set_diff"] == ranking_list_team[i-1]["set_diff"] :
				ranking_list_team[i]["ranking"] = ranking_list_team[i-1]["ranking"]
			else :
				ranking_list_team[i]["ranking"] = i+1
				
	# player ranking
	ranking_list_player = []
	
	rankings_player = getattr(models, f"Ranking_{league.replace(' ', '_')}_player").objects.all().order_by("-POG_point")[0:10]
	
	for ranking_player in rankings_player :
		ranking_list_player.append({"name": ranking_player.name, "nickname": ranking_player.nickname, "team": ranking_player.team, "team_tricode": ranking_player.tricode, "position": ranking_player.position, "POG_point": ranking_player.POG_point})
	
	for i in range(len(ranking_list_player)) :
		if i == 0 :
			ranking_list_player[i]["ranking"] = 1
		else :
			if ranking_list_player[i-1]["POG_point"] == ranking_list_player[i]["POG_point"] :
				ranking_list_player[i]["ranking"] = ranking_list_player[i-1]["ranking"]
			else :
				ranking_list_player[i]["ranking"] = i+1
				
	#print(ranking_list_player)
	
	return render(request, 'ranking.html', {"league": league, "ranking_list_team": ranking_list_team, "ranking_list_player": ranking_list_player})

def champion(request) :
	champions_spring = get_champions("2024", "LCK Spring", 'none')
	champions_MSI = get_champions("2024", "MSI", 'none')
	champions_summer = get_champions("2024", "LCK Summer", 'none')
	
	patch_list_spring = []
	patch_list_MSI = []
	patch_list_summer = []
	
	for champion in champions_spring :
		if champion.patch not in patch_list_spring :
			patch_list_spring.append(champion.patch)
			
	for champion in champions_MSI :
		if champion.patch not in patch_list_MSI :
			patch_list_MSI.append(champion.patch)
		
	if champions_summer != "Error" :
		for champion in champions_summer :
			if champion.patch not in patch_list_summer :
				patch_list_summer.append(champion.patch)
	
	return render(request, "champion.html", {"patch_list_spring": patch_list_spring, "patch_list_MSI": patch_list_MSI, "patch_list_summer": patch_list_summer})

def champion_table(request) :
	year = request.GET.get('year', '')
	league = request.GET.get('league', '')
	patch = request.GET.get('patch', '')
	sort = request.GET.get('sort', '')
	
	print(league)
	champions = get_champions(year, league, patch, sort)
	
	
	if champions == "no_model" :
		return HttpResponse(f"<script>alert(\"Error!\"); window.location.href = \"/champion?league=LCK Summer&patch={league_version}\";</script>")
	
	return render(request, "champion_table.html", {"champions": champions})

def history(request) :
	year = request.GET.get("year", "")
	league = request.GET.get("league", "")
	
	return render(request, "history.js", {"year": year, "league": league})

def Ads(request) :
	return HttpResponse("google.com, pub-9052803485032468, DIRECT, f08c47fec0942fa0", content_type="text/plain")

def naver(request) :
	return render(request, "navered740bad61f2dffe423226b77ebdff35.html")