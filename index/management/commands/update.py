from django.core.management.base import BaseCommand

import index.models

from mwrogue.esports_client import EsportsClient

from datetime import datetime
import pytz
import os

class Command(BaseCommand):
	help = 'update command!'
	UTC = pytz.timezone("UTC")
	KST = pytz.timezone("Asia/Seoul")
	site = EsportsClient("lol")
	## 받으려는 대회의 LeaguePedia에서의 대회 이름 지정
	league = "LCK 2024 Regional Finals"
	year = 2024
	base_path = os.getenv("LCKINFO_HOME")
	
	def update_schedule(self) :
		schedules = self.site.cargo_client.query(
			tables="Tournaments=T, MatchSchedule=MS",
			join_on="T.OverviewPage=MS.OverviewPage",
			where=f"T.Name LIKE '%{self.__class__.league}%'",
			order_by="MS.DateTime_UTC",
			limit=400,
			
			fields="T.Name, MS.Team1, MS.Team2, MS.Team1Score, MS.Team2Score, MS.DateTime_UTC",
		)
		
		if len(schedules) == 0 :
			print("There is no schedule to record")
		
		for schedule in schedules :
			schedule["DateTime UTC"] = datetime.strptime(schedule["DateTime UTC"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=self.UTC).astimezone(self.KST).replace(tzinfo=None)
			
			schedule_obj, created = getattr(index.models, f"Schedule_{self.__class__.year}").objects.get_or_create(
				date=schedule["DateTime UTC"],
			)
			
			if "Regional Finals" in schedule["Name"] :
				schedule_obj.team1_name=getattr(self, f"convert_team_name_to_Korean_LCK_2024_Summer")(schedule["Team1"])
				schedule_obj.team2_name=getattr(self, f"convert_team_name_to_Korean_LCK_2024_Summer")(schedule["Team2"])
				schedule_obj.team1_tricode=getattr(self, f"convert_team_name_to_tricode_LCK_2024_Summer")(schedule["Team1"])
				schedule_obj.team2_tricode=getattr(self, f"convert_team_name_to_tricode_LCK_2024_Summer")(schedule["Team2"])
			else :
				schedule_obj.team1_name=getattr(self, f"convert_team_name_to_Korean_{self.__class__.league.replace(' ', '_')}")(schedule["Team1"])
				schedule_obj.team2_name=getattr(self, f"convert_team_name_to_Korean_{self.__class__.league.replace(' ', '_')}")(schedule["Team2"])
				schedule_obj.team1_tricode=getattr(self, f"convert_team_name_to_tricode_{self.__class__.league.replace(' ', '_')}")(schedule["Team1"])
				schedule_obj.team2_tricode=getattr(self, f"convert_team_name_to_tricode_{self.__class__.league.replace(' ', '_')}")(schedule["Team2"])
			
			if "Regional Finals" in schedule["Name"] :
				tournament = "선발전"
			elif "LCK" in schedule["Name"] :
				tournament = schedule["Name"].split(" ")[0] + " " + schedule["Name"].split(" ")[2]
			elif "MSI" in schedule["Name"] or "Worlds" in schedule["Name"] :
				tournament = schedule["Name"].split(" ")[0]
			else :
				tournament = "unknown"
			schedule_obj.tournament = tournament

			
			if schedule["Team1Score"] == None or schedule["Team2Score"] == None :
				schedule["Team1Score"] = '0'
				schedule["Team2Score"] = '0'
			
			schedule_obj.team1_score = int(schedule["Team1Score"])
			schedule_obj.team2_score = int(schedule["Team2Score"])
				
			print(f"recording {schedule}")
			schedule_obj.save()
	
	def update_champion(self) :
		pickbans = self.site.cargo_client.query(
			tables="Tournaments=T, ScoreboardGames=SG",
			where=f"T.Name LIKE '%{self.__class__.league}%'",
			join_on="T.Name=SG.Tournament",
			order_by="SG.DateTime_UTC",
			limit=400,
			
			fields="SG.Winner, SG.Team1Bans, SG.Team2Bans, SG.Team1Picks, SG.Team2Picks, SG.Patch, SG.DateTime_UTC",
		)
		
		if len(pickbans) == 0 :
			print("There is no pickban to record")
			
		# Get champion model
		champion_DB = getattr(index.models, f"Champion_{self.__class__.league.replace(' ', '_')}")
		
		for pickban in pickbans :
			if pickban["Winner"] == None :
				continue
			
			# check whether the log is after last_update.
			pickban["DateTime_UTC"] = datetime.strptime(pickban["DateTime UTC"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=self.UTC).astimezone(self.KST).replace(tzinfo=None)
			
			with open(f"{self.__class__.base_path}/index/management/commands/last_update_champion.txt", "r") as file :
				last_update = datetime.strptime(file.read(), "%Y-%m-%d %H:%M:%S")
			
			if not pickban["DateTime_UTC"] > last_update :
				continue
			
			## 2024 LCK spring 14.1 -> 14.1b
			#if pickban["Patch"] == "14.1" :
			#	if pickban["DateTime_UTC"] > datetime(2024, 1, 23) :
			#		pickban["Patch"] = "14.1b"
			
			bans = []
			team1Picks = []
			team2Picks = []
			patch = pickban["Patch"]
			
			bans.extend(pickban["Team1Bans"].split(","))
			bans.extend(pickban["Team2Bans"].split(","))
			
			team1Picks.extend(pickban["Team1Picks"].split(","))
			team2Picks.extend(pickban["Team2Picks"].split(","))
			
			# Add ban
			for ban in bans :
				ban = self.convert_champions_name(ban)
				champion_obj, created = champion_DB.objects.get_or_create(name=ban, patch=patch)
				
				champion_obj.ban += 1
				champion_obj.save()
			
			# Add pick, win, lose
			for team1Pick in team1Picks :
				team1Pick = self.convert_champions_name(team1Pick)
				champion_obj, created = champion_DB.objects.get_or_create(name=team1Pick, patch=patch)
				
				champion_obj.pick += 1
				if int(pickban["Winner"]) == 1 :
					champion_obj.win += 1
					champion_obj.save()
				else :
					champion_obj.lose += 1
					champion_obj.save()
					
			for team2Pick in team2Picks :
				team2Pick = self.convert_champions_name(team2Pick)
				champion_obj, created = champion_DB.objects.get_or_create(name=team2Pick, patch=patch)
				
				champion_obj.pick += 1
				if int(pickban["Winner"]) == 2 :
					champion_obj.win += 1
					champion_obj.save()
				else :
					champion_obj.lose += 1
					champion_obj.save()
			
			print(f"recording {pickban}")		
			
			# Update last_update.txt
			with open(f"{self.__class__.base_path}/index/management/commands/last_update_champion.txt", "w") as file :
				file.write(pickban["DateTime_UTC"].strftime("%Y-%m-%d %H:%M:%S"))
	
	def update_ranking(self) :
		convert_Korean_team_name_to_tricode = getattr(self, f"convert_Korean_team_name_to_tricode_{self.__class__.league.replace(' ', '_')}")
		
		class Team :
			def __init__(self, name) :
				self.name = name
				self.tricode = convert_Korean_team_name_to_tricode(self.name)
				self.match_win = 0
				self.match_lose = 0
				self.set_win = 0
				self.set_lose = 0
		
		schedules = getattr(index.models, "Schedule").objects.filter(date__gt=datetime(2024,1,1), date__lt=datetime(2024,8,19), tournament=self.__class__.league)
		
		teams = []
		team_names_Korean = getattr(self, f"team_name_Korean_{self.__class__.league.replace(' ', '_')}")
		for team in team_names_Korean :
			teams.append(Team(team))
		
		for schedule in schedules :
			for team in teams :
				if schedule.team1_name == team.name :
					team1 = team
					continue
			for team in teams :
				if schedule.team2_name == team.name :
					team2 = team
					continue

			
			# match score
			if schedule.team1_score == 0 and schedule.team2_score == 0 :
				continue
			else :
				if schedule.team1_score > schedule.team2_score :
					team1.match_win += 1
					team2.match_lose += 1
				elif schedule.team1_score < schedule.team2_score :
					team2.match_win += 1
					team1.match_lose += 1
				else :
					continue
			
			# set score
			team1.set_win += schedule.team1_score
			team1.set_lose += schedule.team2_score
			
			team2.set_win += schedule.team2_score	
			team2.set_lose += schedule.team1_score
		
		# Get standing model
		standing_model = getattr(index.models, f"Ranking_{self.__class__.league.replace(' ', '_')}")
		
		for team in teams :
			standing_obj = standing_model.objects.get(name=team.name)
			
			print(f"recording {team.name}")
			
			standing_obj.tricode = team.tricode
			standing_obj.set_win = team.set_win
			standing_obj.set_lose = team.set_lose
			standing_obj.match_win = team.match_win
			standing_obj.match_lose = team.match_lose
			
			standing_obj.save()
	
	def update_ranking_player(self) :
		# Get MVP list
		mvps = self.site.cargo_client.query(
			tables="MatchScheduleGame=MSG, ScoreboardGames=SG",
			join_on="MSG.GameId=SG.GameId",
			order_by="SG.DateTime_UTC",
			where=f"SG.Tournament='{self.__class__.league}'",
			limit=400,
			
			fields="MSG.MVP, SG.DateTime_UTC",
		)
		
		if len(mvps) == 0 :
			print("There is no mvps (no match) to record")
			
		# Get ranking_player model
		ranking_player_DB = getattr(index.models, f"Ranking_{self.__class__.league.replace(' ', '_')}_player")
		
		for mvp in mvps :
			# check whether the log is after last_update.
			mvp["DateTime UTC"] = datetime.strptime(mvp["DateTime UTC"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=self.UTC).astimezone(self.KST).replace(tzinfo=None)
			
			with open(f"{self.__class__.base_path}/index/management/commands/last_update_player_ranking.txt", "r") as file :
				last_update = datetime.strptime(file.read(), "%Y-%m-%d %H:%M:%S")
			
			if not mvp["DateTime UTC"] > last_update :
				continue
			
			# MVP nickname
			mvp_nickname = mvp["MVP"].split(' ')[0]
			
			# Get MVP info
			print(mvp_nickname)
			ranking_player_obj, created = ranking_player_DB.objects.get_or_create(nickname=mvp_nickname)
			
			ranking_player_obj.POG_point += 100
			ranking_player_obj.save()
			
			# Update last_update.txt
			with open(f"{self.__class__.base_path}/index/management/commands/last_update_player_ranking.txt", "w") as file :
				file.write(mvp["DateTime UTC"].strftime("%Y-%m-%d %H:%M:%S"))
	
	
	def convert_team_name_to_tricode_LCK_2024_Spring(self, team) :
		teams = {
			"Gen.G":"GEN",
			"T1":"T1",
			"Hanwha Life Esports":"HLE",
			"Dplus KIA":"DK",
			"KT Rolster":"KT",
			"Nongshim RedForce":"NS",
			"DRX":"DRX",
			"OKSavingsBank BRION":"BRO",
			"Kwangdong Freecs":"KDF",
			"FearX":"FOX",
		}
		
		if team in teams :
			return teams[team]
		else :
			return team
	
	def convert_team_name_to_Korean_LCK_2024_Spring(self, team) :
		teams = {
			"Gen.G":"젠지",
			"T1":"T1",
			"Hanwha Life Esports":"한화생명e스포츠",
			"Dplus KIA":"디플러스 기아",
			"KT Rolster":"KT 롤스터",
			"Nongshim RedForce":"농심 레드포스",
			"DRX":"DRX",
			"OKSavingsBank BRION":"OK저축은행 브리온",
			"Kwangdong Freecs":"광동 프릭스",
			"FearX":"FearX",
		}
		
		if team in teams :
			return teams[team]
		else :
			return team
	
	
	def convert_team_name_to_tricode_MSI_2024(self, team) :
		teams = {
			"Gen.G":"GEN",
			"T1":"T1",
			"Bilibili Gaming":"BLG",
			"G2 Esports":"G2",
			"Team Liquid":"TL",
			"Top Esports":"TES",
			"PSG Talon":"PSG",
			"Fnatic":"FNC",
			"GAM Esports":"GAM",
			"FlyQuest":"FLY",
			"LOUD":"LOUD",
			"Estral Esports":"EST",
		}
		
		if team in teams :
			return teams[team]
		else :
			return team

	def convert_team_name_to_Korean_MSI_2024(self, team) :
		teams = {
			"Gen.G":"젠지",
			"T1":"T1",
			"Bilibili Gaming":"Bilibili Gaming",
			"G2 Esports":"G2 Esports",
			"Team Liquid":"Team Liquid",
			"Top Esports":"Top Esports",
			"PSG Talon":"PSG Talon",
			"Fnatic":"Fnatic",
			"GAM Esports":"GAM Esports",
			"FlyQuest":"FlyQuest",
			"LOUD":"LOUD",
			"Estral Esports":"Estral Esports",
		}
		
		if team in teams :
			return teams[team]
		else :
			return team
	
	
	def convert_team_name_to_Korean_LCK_2024_Summer(self, team) :
		teams = {
			"Gen.G":"젠지",
			"T1":"T1",
			"Hanwha Life Esports":"한화생명e스포츠",
			"Dplus KIA":"디플러스 기아",
			"KT Rolster":"KT 롤스터",
			"Nongshim RedForce":"농심 레드포스",
			"DRX":"DRX",
			"OKSavingsBank BRION":"OK저축은행 브리온",
			"Kwangdong Freecs":"광동 프릭스",
			"BNK FearX":"BNK 피어엑스",
		}
		
		if team in teams :
			return teams[team]
		elif team == None :
			return "None"
		else :
			return team
		
	def convert_team_name_to_tricode_LCK_2024_Summer(self, team) :
		teams = {
			"Gen.G":"GEN",
			"T1":"T1",
			"Hanwha Life Esports":"HLE",
			"Dplus KIA":"DK",
			"KT Rolster":"KT",
			"Nongshim RedForce":"NS",
			"DRX":"DRX",
			"OKSavingsBank BRION":"BRO",
			"Kwangdong Freecs":"KDF",
			"BNK FearX":"FOX",
		}
		
		if team in teams :
			return teams[team]
		else :
			return team
	
	team_name_Korean_LCK_2024_Summer = [
		"젠지",
		"T1",
		"한화생명e스포츠",
		"디플러스 기아",
		"KT 롤스터",
		"농심 레드포스",
		"DRX",
		"OK저축은행 브리온",
		"광동 프릭스",
		"BNK 피어엑스",	
	]
	
	
	def convert_champions_name(self, name) :
		try :
			names = {
				"Aatrox": "아트록스",
				"Ahri": "아리",
				"Akali": "아칼리",
				"Akshan": "아크샨",
				"Alistar": "알리스타",
				"Amumu": "아무무",
				"Anivia": "애니비아",
				"Annie": "애니",
				"Aphelios": "아펠리오스",
				"Ashe": "애쉬",
				"Aurelion Sol": "아우렐리온 솔",
				"Aurora": "오로라",
				"Azir": "아지르",
				"Bard": "바드",
				"Briar": "브라이어",
				"Bel'Veth": "벨베스",
				"Blitzcrank": "블리츠크랭크",
				"Brand": "브랜드",
				"Braum": "브라움",
				"Caitlyn": "케이틀린",
				"Camille": "카밀",
				"Cassiopeia": "카시오페아",
				"Cho'Gath": "초가스",
				"Corki": "코르키",
				"Darius": "다리우스",
				"Diana": "다이애나",
				"Dr. Mundo": "문도 박사",
				"Draven": "드레이븐",
				"Ekko": "에코",
				"Elise": "엘리스",
				"Evelynn": "이블린",
				"Ezreal": "이즈리얼",
				"Fiddlesticks": "피들스틱",
				"Fiora": "피오라",
				"Fizz": "피즈",
				"Galio": "갈리오",
				"Gangplank": "갱플랭크",
				"Garen": "가렌",
				"Gnar": "나르",
				"Gragas": "그라가스",
				"Graves": "그레이브즈",
				"Gwen": "그웬",
				"Hecarim": "헤카림",
				"Heimerdinger": "하이머딩거",
				"Hwei": "흐웨이",
				"Illaoi": "일라오이",
				"Irelia": "이렐리아",
				"Ivern": "아이번",
				"Janna": "잔나",
				"Jarvan IV": "자르반 4세",
				"Jax": "잭스",
				"Jayce": "제이스",
				"Jhin": "진",
				"Jinx": "징크스",
				"Kai'Sa": "카이사",
				"Kalista": "칼리스타",
				"Karma": "카르마",
				"Karthus": "카서스",
				"Kassadin": "카사딘",
				"Katarina": "카타리나",
				"Kayle": "케일",
				"Kayn": "케인",
				"Kennen": "케넨",
				"Kha'Zix": "카직스",
				"Kindred": "킨드레드",
				"Kled": "클레드",
				"Kog'Maw": "코그모",
				"K'Sante": "크산테",
				"LeBlanc": "르블랑",
				"Lee Sin": "리 신",
				"Leona": "레오나",
				"Lillia": "릴리아",
				"Lissandra": "리산드라",
				"Lucian": "루시안",
				"Lulu": "룰루",
				"Lux": "럭스",
				"Malphite": "말파이트",
				"Malzahar": "말자하",
				"Maokai": "마오카이",
				"Master Yi": "마스터 이",
				"Milio": "밀리오",
				"Miss Fortune": "미스 포츈",
				"Mordekaiser": "모데카이저",
				"Morgana": "모르가나",
				"Naafiri": "나피리",
				"Nami": "나미",
				"Nasus": "나서스",
				"Nautilus": "노틸러스",
				"Neeko": "니코",
				"Nidalee": "니달리",
				"Nilah": "닐라",
				"Nocturne": "녹턴",
				"Nunu & Willump": "누누와 윌럼프",
				"Olaf": "올라프",
				"Orianna": "오리아나",
				"Ornn": "오른",
				"Pantheon": "판테온",
				"Poppy": "뽀삐",
				"Pyke": "파이크",
				"Qiyana": "키아나",
				"Quinn": "퀸",
				"Rakan": "라칸",
				"Rammus": "람머스",
				"Rek'Sai": "렉사이",
				"Rell": "렐",
				"Renata Glasc": "레나타 글라스크",
				"Renekton": "레넥톤",
				"Rengar": "레인저",
				"Riven": "리븐",
				"Rumble": "럼블",
				"Ryze": "라이즈",
				"Samira": "사미라",
				"Sejuani": "세주아니",
				"Senna": "세나",
				"Seraphine": "세라핀",
				"Sett": "세트",
				"Shaco": "샤코",
				"Shen": "쉔",
				"Shyvana": "쉬바나",
				"Singed": "신지드",
				"Sion": "사이온",
				"Sivir": "시비르",
				"Skarner": "스카너",
				"Smolder": "스몰더",
				"Sona": "소나",
				"Soraka": "소라카",
				"Swain": "스웨인",
				"Sylas": "사일러스",
				"Syndra": "신드라",
				"Tahm Kench": "탐 켄치",
				"Taliyah": "탈리야",
				"Talon": "탈론",
				"Taric": "타릭",
				"Teemo": "티모",
				"Thresh": "쓰레쉬",
				"Tristana": "트리스타나",
				"Trundle": "트런들",
				"Tryndamere": "트린다미어",
				"Twisted Fate": "트위스티드 페이트",
				"Twitch": "트위치",
				"Udyr": "우디르",
				"Urgot": "우르곳",
				"Varus": "바루스",
				"Vayne": "베인",
				"Veigar": "베이가",
				"Vel'Koz": "벨코즈",
				"Vex": "벡스",
				"Vi": "바이",
				"Viego": "비에고",
				"Viktor": "빅토르",
				"Vladimir": "블라디미르",
				"Volibear": "볼리베어",
				"Warwick": "워윅",
				"Wukong": "오공",
				"Xayah": "자야",
				"Xerath": "제라스",
				"Xin Zhao": "신 짜오",
				"Yasuo": "야스오",
				"Yone": "요네",
				"Yorick": "요릭",
				"Yuumi": "유미",
				"Zac": "자크",
				"Zed": "제드",
				"Zeri": "제리",
				"Ziggs": "직스",
				"Zilean": "질리언",
				"Zoe": "조이",
				"Zyra": "자이라",
				"None": "미정",
			}
		except KeyError :
			print(name)
		
		return names[name]
	
	def handle(self, *args, **options):
		print("start to update schedule...")
		self.update_schedule()
		print("updating schedule complete!")
		print("start to update champion...")
		self.update_champion()
		print("updating champion complete!")
		print("start to update ranking_2024_LCK_summer...")
		self.update_ranking()
		print("updating ranking_2024_LCK_summer complete")
		print("start to update ranking_2024_LCK_summer_player...")
		self.update_ranking_player()
		print("updating ranking_2024_LCK_summer_player complete!")
		