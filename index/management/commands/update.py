from django.core.management.base import BaseCommand

from index.models import Schedule
from index.models import Ranking_23_summer_regular
from index.models import Champion
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import time

class Command(BaseCommand):
    help = 'update command!'
    
    def update_schedule(self) :
        # Setting web driver
        url = "https://lolesports.com/schedule?leagues=lck"
        
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")
        option.add_argument("--lang=ko_KR")
        
        driver = webdriver.Chrome(option)
        
        # driver get URL 
        driver.get(url)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(3)
        
        # driver get schedule from lol wiki
        while True :
            web_source = driver.page_source
            soup_origin = BeautifulSoup(web_source, "html.parser")
            event = soup_origin.find("div", class_="Event")
            if event != None :
                break
        
        # quit driver
        driver.quit()
        
        # get schedule information
        event_tags = event.find_all("div")
        for event_tag in event_tags :
            
            # EventDate
            if event_tag['class'][0] == "EventDate" :
                monthday = event_tag.find("span", class_="monthday")
            
                year = 2023 # year 이 부분 생각 필요
                month = int(monthday.text.split('월')[0])   # month
                day_temp = monthday.text.split(' ')[1]
                day = int(day_temp[:-1])    # day
                weekday_datetime = datetime(year, month, day).weekday()
                days = ['월', '화', '수', '목', '금', '토', '일']
                weekday = days[weekday_datetime]    # weekday
            
            # EventTime
            elif event_tag['class'][0] == "EventMatch" :
                # continue if the Match is about live
                a = event_tag.find("a")
                if a != None :
                    if a['href'].find("live") != -1 :
                        continue
                
                EventTime = event_tag.find("div", class_="EventTime")

                hour = int(EventTime.find("span", class_="hour").text)  # hour
                min = EventTime.find("span", class_="minute")   # min
                if min == None :
                    min = 0
                else :
                    min = int(min.text)
                ampm = EventTime.find("span", class_="ampm").text   # ampm

                # EventTeam
                teams_tag = event_tag.find("div", class_="teams")
                    
                team1 = teams_tag.find("div", class_="team1")
                team1_name = team1.find("span", class_="name").text
                team1_name = self.convert_team_name_23_summer(team1_name)
                team1_tricode = team1.find("span", class_="tricode")
                
                team2 = teams_tag.find("div", class_="team2")
                team2_name = team2.find("span", class_="name").text
                team2_name = self.convert_team_name_23_summer(team2_name)
                team2_tricode = team2.find("span", class_="tricode")
                
                if teams_tag.find("div", class_="score") != None :
                    score = teams_tag.find("div", class_="score")
                    team1_score = score.find("span", class_="scoreTeam1").text
                    team2_score = score.find("span", class_="scoreTeam2").text
                else :
                    team1_score = 0
                    team2_score = 0
                
                date = datetime(year, month, day, hour, min)
                
                # etc
                if date < datetime(2023, 6, 7) :
                    etc = "LCK spring"
                elif date >= datetime(2023, 6, 7) and date <= datetime(2023, 7, 7, 17, 0) :
                    etc = "LCK summer 정규시즌 1라운드"
                elif date > datetime(2023, 7, 7, 17, 0) and date <= datetime(2023, 8, 6, 17, 30) :
                    etc = "LCK summer 정규시즌 2라운드"
                else :
                    etc = "LCK summer 플레이오프"
                    
                # update or create schedule DB
                try :
                    schedule = Schedule.objects.get(year=year, month=month, day=day, weekday=weekday, team1_name=team1_name, team2_name=team2_name, team1_tricode=team1_tricode.text, team2_tricode=team2_tricode.text, hour=hour, min=min, ampm=ampm, etc=etc)
                        
                    # If there is a data that is suit for the date.
                    if schedule.team1_score != team1_score or schedule.team2_score != team2_score :
                        
                        # If there is a data that is suit for date and result.
                        continue
                    else :
                        
                        # If there is a data that is suit for date but is not suit for result.
                        schedule.team1_score = team1_score
                        schedule.team2_score = team2_score
                        schedule.save()
                            
                except Schedule.DoesNotExist :
                    # If there is a no data that is suit for the date.
                    Schedule.objects.create(year=year, month=month, day=day, weekday=weekday, team1_name=team1_name, team2_name=team2_name, team1_tricode=team1_tricode.text, team2_tricode=team2_tricode.text, team1_score=team1_score, team2_score=team2_score, hour=hour, min=min, ampm=ampm, etc=etc)
                
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
        
    def update_champion(self) :
        URL = "https://lol.fandom.com/wiki/LCK/2023_Season/Summer_Season/Match_History"
        
        # Setting web driver
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")
        option.add_argument("--lang=ko_KR")
        
        driver = webdriver.Chrome(option)
        
        # driver get URL
        driver.get(URL)
        
        # get champions table from lol wiki
        while True :
            driver.implicitly_wait(5)
            web_source = driver.page_source
            soup_origin = BeautifulSoup(web_source, "html.parser")
            table = soup_origin.find("table", class_="wikitable hoverable-multirows mhgame sortable plainlinks column-show-hide-1 jquery-tablesorter")
            if table != None :
                break
        
        # quit driver
        driver.quit()
        
        
        tbody = table.find("tbody")
        match_histories = tbody.find_all("tr")
        for match_history in match_histories :
            td = match_history.find_all("td")
            
            today = td[0].text
            #if str(datetime.now().date()) != today :
            #    continue
            
            patch = td[1].text
            team1 = td[2].find("a").get("data-to-id")
            team2 = td[3].find("a").get("data-to-id")
            
            winner_team = td[4].find("a").get("data-to-id")
            winner_team_no = 0
            
            if winner_team == team1 :
                winner_team_no = 1
            else :
                winner_team_no = 2
            
            champion_ban_spans = td[5].find_all("span")
            champion_ban_spans.extend(td[6].find_all("span"))
            for champion_ban_span in champion_ban_spans :
                champion_ban = champion_ban_span.get("title")
                champion_ban = self.convert_champions_name(champion_ban)
                champion_object, created = Champion.objects.get_or_create(name=champion_ban, patch=patch)
                champion_object.ban += 1
                champion_object.save()
                
            champion_pick_team1_spans = td[7].find_all("span")
            champion_pick_team2_spans = td[8].find_all("span")
            if winner_team_no == 1 :
                for champion_pick_span in champion_pick_team1_spans :
                    champion_pick = champion_pick_span.get("title")
                    champion_pick = self.convert_champions_name(champion_pick)
                    champion_object, created = Champion.objects.get_or_create(name=champion_pick, patch=patch)
                    champion_object.pick += 1
                    champion_object.win += 1
                    champion_object.save()
            
                for champion_pick_span in champion_pick_team2_spans :
                    champion_pick = champion_pick_span.get("title")
                    champion_pick = self.convert_champions_name(champion_pick)
                    champion_object, created = Champion.objects.get_or_create(name=champion_pick, patch=patch)
                    champion_object.pick += 1
                    champion_object.lose += 1
                    champion_object.save()
                    
            else :
                for champion_pick_span in champion_pick_team1_spans :
                    champion_pick = champion_pick_span.get("title")
                    champion_pick = self.convert_champions_name(champion_pick)
                    champion_object, created = Champion.objects.get_or_create(name=champion_pick, patch=patch)
                    champion_object.pick += 1
                    champion_object.lose += 1
                    champion_object.save()
            
                for champion_pick_span in champion_pick_team2_spans :
                    champion_pick = champion_pick_span.get("title")
                    champion_pick = self.convert_champions_name(champion_pick)
                    champion_object, created = Champion.objects.get_or_create(name=champion_pick, patch=patch)
                    champion_object.pick += 1
                    champion_object.win += 1
                    champion_object.save()
                
    def convert_team_name_23_summer(self, team) :
        teams = {
            "Gen.G": "젠지",
            "T1": "T1",
            "kt Rolster": "kt 롤스터",
            "Hanwha Life Esports": "한화생명e스포츠",
            "Dplus Kia": "디플러스 기아",
            "Liiv SANDBOX": "리브 샌드박스",
            "Kwangdong Freecs": "광동 프릭스",
            "OKSavingsBank BRION": "OK저축은행 브리온",
            "DRX": "DRX",
            "NongShim REDFORCE": "농심 레드포스",
            "TBD": "미정"
        }
        
        return teams[team]

    def reset_ranking_23_summer_regular(self) :
        teams = ["T1", "GEN", "HLE", "KDF", "LSB", "NS", "DK", "DRX", "BRO", "KT"]
        
        for team in teams :
            team_object = Ranking_23_summer_regular.objects.get(tricode=team)
            team_object.game_win = 0
            team_object.game_lose = 0
            team_object.set_win = 0
            team_object.set_lose = 0
            
            team_object.save()

    def update_ranking_23_summer_regular(self) :
        self.reset_ranking_23_summer_regular()
        
        schedule_objects = Schedule.objects.all()
        for schedule_object in schedule_objects :
            if ("LCK summer 정규시즌" in schedule_object.etc) and schedule_object.year == 2023:
                team1 = Ranking_23_summer_regular.objects.get(name=schedule_object.team1_name)
                team2 = Ranking_23_summer_regular.objects.get(name=schedule_object.team2_name)
                
                # when the schedule is not started yet
                if schedule_object.team1_score == 0 and schedule_object.team2_score == 0 :
                    continue
                
                # update game_win, game_lose
                if schedule_object.team1_score > schedule_object.team2_score :
                    team1.game_win += 1
                    team2.game_lose += 1
                else :
                    team1.game_lose += 1
                    team2.game_win += 1
                
                # update set_win, set_lose
                team1.set_win += schedule_object.team1_score
                team1.set_lose += schedule_object.team2_score
                team2.set_win += schedule_object.team2_score
                team2.set_lose += schedule_object.team1_score
            
                # apply update
                team1.save()
                team2.save()

    def handle(self, *args, **options):
        self.update_schedule()
        self.update_champion()
