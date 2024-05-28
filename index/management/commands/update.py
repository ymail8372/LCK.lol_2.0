from django.core.management.base import BaseCommand

import index.models
from index.models import Schedule

from mwrogue.esports_client import EsportsClient

from datetime import datetime
import pytz

class Command(BaseCommand):
	help = 'update command!'
	UTC = pytz.timezone("UTC")
	KST = pytz.timezone("Asia/Seoul")
	site = EsportsClient("lol")
	
	def update_schedule(self) :
		league = "MSI 2024"
		
		schedules = self.site.cargo_client.query(
			tables="Tournaments=T, MatchSchedule=MS",
			join_on="T.OverviewPage=MS.OverviewPage",
			where=f"T.Name LIKE '%{league}%'",
			order_by="MS.DateTime_UTC",
			limit=400,
			
			fields="T.Name, MS.Team1, MS.Team2, MS.Team1Score, MS.Team2Score, MS.DateTime_UTC, MS.MVP, MS.MVPPoints",
		)
		
		for schedule in schedules :
			schedule["DateTime UTC"] = datetime.strptime(schedule["DateTime UTC"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=self.UTC).astimezone(self.KST).replace(tzinfo=None)
			schedule_obj, created = Schedule.objects.get_or_create(
				team1_name=getattr(self, f"convert_team_name_to_Korean_{league.replace(' ', '_')}")(schedule["Team1"]),
				team2_name=getattr(self, f"convert_team_name_to_Korean_{league.replace(' ', '_')}")(schedule["Team2"]),
				team1_tricode=getattr(self, f"convert_team_name_to_tricode_{league.replace(' ', '_')}")(schedule["Team1"]),
				team2_tricode=getattr(self, f"convert_team_name_to_tricode_{league.replace(' ', '_')}")(schedule["Team2"]),
				date=schedule["DateTime UTC"],
			)
			
			# set schedule.tournament
			if created :
				schedule_obj.tournament=schedule["Name"]
			
			if schedule_obj.team1_score == int(schedule["Team1Score"]) and schedule_obj.team2_score == int(schedule["Team2Score"]) :
				print("continue")
				continue
			else :
				print(f"recording {schedule}")
				schedule_obj.team1_score = schedule["Team1Score"]
				schedule_obj.team2_score = schedule["Team2Score"]
				
				schedule_obj.save()
	
	def update_champion(self) :
		league = "MSI 2024"
		
		pickbans = self.site.cargo_client.query(
			tables="Tournaments=T, ScoreboardGames=SG",
			where=f"T.Name LIKE '%{league}%'",
			join_on="T.Name=SG.Tournament",
			order_by="SG.DateTime_UTC",
			limit=400,
			
			fields="SG.Winner, SG.Team1Bans, SG.Team2Bans, SG.Team1Picks, SG.Team2Picks, SG.Patch, SG.DateTime_UTC",
		)
		
		# Get champion model
		champion_DB = getattr(index.models, f"Champion_{league.replace(' ', '_')}")
		
		for pickban in pickbans :
			# check whether the log is after last_update.
			# /srv/LCK.lol_2.0/index/management/commands/last_update.txt
			pickban["DateTime_UTC"] = datetime.strptime(pickban["DateTime UTC"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=self.UTC).astimezone(self.KST).replace(tzinfo=None)
			
			with open("./index/management/commands/last_update_champion.txt", "r") as file :
				last_update = datetime.strptime(file.read(), "%Y-%m-%d %H:%M:%S")
			
			if not pickban["DateTime_UTC"] > last_update :
				print("continue")
				continue
			
			# 2024 LCK spring 14.1 -> 14.1b
			if pickban["Patch"] == "14.1" :
				if pickban["DateTime_UTC"] > datetime(2024, 1, 23) :
					pickban["Patch"] = "14.1b"
			
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
				#print(f"{champion.name} updated")
				champion_obj.save()
			
			# Add pick, win, lose
			for team1Pick in team1Picks :
				team1Pick = self.convert_champions_name(team1Pick)
				champion_obj, created = champion_DB.objects.get_or_create(name=team1Pick, patch=patch)
				
				champion_obj.pick += 1
				if int(pickban["Winner"]) == 1 :
					champion_obj.win += 1
					#print(f"{champion.name} updated")
					champion_obj.save()
				else :
					champion_obj.lose += 1
					#print(f"{champion.name} updated")
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
			with open("./index/management/commands/last_update_champion.txt", "w") as file :
				print(pickban["DateTime_UTC"].strftime("%Y-%m-%d %H:%M:%S"))
				file.write(pickban["DateTime_UTC"].strftime("%Y-%m-%d %H:%M:%S"))
	
	def update_ranking_2024_LCK_spring(self) :
		league = "LCK 2024 spring"
		
		standings = self.site.cargo_client.query(
			tables="Tournaments=T, Standings=S",
			where=f"T.Name='{league}'",
			join_on="T.OverviewPage=S.OverviewPage",
			order_by="S.Place",
			limit=400,
			
			fields="T.Name, S.Team, S.Place, S.WinSeries, S.LossSeries, S.WinGames, S.LossGames",
		)
		
		# Get standing model
		standing_DB = getattr(index.models, f"Ranking_{league.replace(' ', '_')}")
		
		for standing in standings :
			standing_obj, created = standing_DB.objects.get_or_create(name=standing["Team"])
			
			if standing["WinGames"] == standing_obj.set_win and standing["LossGames"] == standing_obj.set_lose :
				print("continue")
				continue
			
			print(f"recording {standing}")
			
			standing_obj.tricode = getattr(self, f"convert_team_name_to_tricode_{league.replace(' ', '_')}")(standing["Team"])
			standing_obj.set_win = standing["WinGames"]
			standing_obj.set_lose = standing["LossGames"]
			standing_obj.match_win = standing["WinSeries"]
			standing_obj.match_lose = standing["LossSeries"]
			
			standing_obj.save()
	
	def update_ranking_2024_LCK_spring_player(self) :
		league = "LCK 2024 spring"
		
		# Get MVP list
		mvps = self.site.cargo_client.query(
			tables="MatchScheduleGame=MSG, ScoreboardGames=SG",
			join_on="MSG.GameId=SG.GameId",
			order_by="SG.DateTime_UTC",
			where=f"SG.Tournament='LCK 2024 spring'",
			limit=400,
			
			fields="MSG.MVP, SG.DateTime_UTC",
		)
		
		# Get ranking_player model
		ranking_player_DB = getattr(index.models, f"Ranking_{league.replace(' ', '_')}_player")
		
		for mvp in mvps :
			# check whether the log is after last_update.
			mvp["DateTime UTC"] = datetime.strptime(mvp["DateTime UTC"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=self.UTC).astimezone(self.KST).replace(tzinfo=None)
			
			with open("./index/management/commands/last_update_player_ranking.txt", "r") as file :
				last_update = datetime.strptime(file.read(), "%Y-%m-%d %H:%M:%S")
			
			if not mvp["DateTime UTC"] > last_update :
				print("continue")
				continue
			
			# MVP ID
			mvp_ID = mvp["MVP"].split(' ')[0]
			
			# Get MVP info
			player_ranking = self.site.cargo_client.query(
				tables="Players=P",
				where=f"P.ID='{mvp_ID}' and P.Country='South Korea' and P.IsRetired='No'",
				limit=30,
				
				fields="P.ID, P.NativeName, P.Team, P.Role",
			)
			
			ranking_player_obj, created = ranking_player_DB.objects.get_or_create(
				nickname=player_ranking[0]["ID"],
				name=player_ranking[0]["NativeName"],
				team=player_ranking[0]["Team"],
				position=player_ranking[0]["Role"]
			)
			
			ranking_player_obj.tricode = getattr(self, f"convert_team_name_to_tricode_{league.replace(' ', '_')}")(player_ranking[0]["Team"])
			ranking_player_obj.POG_point += 100
			
			ranking_player_obj.save()
			
			print(f"{player_ranking}")
			
			# Update last_update.txt
			with open("./index/management/commands/last_update_player_ranking.txt", "w") as file :
				print(mvp["DateTime UTC"].strftime("%Y-%m-%d %H:%M:%S"))
				file.write(mvp["DateTime UTC"].strftime("%Y-%m-%d %H:%M:%S"))
	
	
	def convert_team_name_to_tricode_LCK_2024_spring(self, team) :
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
	
	def convert_team_name_to_Korean_LCK_2024_spring(self, team) :
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
	
	def convert_team_name_to_tricode_LCK_2024_summer(self, team) :
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
	
	def convert_team_name_to_Korean_LCK_2024_summer(self, team) :
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
		#print("start to update schedule...")
		#self.update_schedule()
		#print("updating schedule complete!")
		print("start to update champion...")
		self.update_champion()
		print("updating champion complete!")
		#print("start to update ranking_2024_LCK_spring...")
		#self.update_ranking_2024_LCK_spring()
		#print("updating ranking_2024_LCK_spring complete")
		#print("start to update ranking_2024_LCK_spring_player...")
		#self.update_ranking_2024_LCK_spring_player()
		#print("updating ranking_2024_LCK_spring_player complete!")
		