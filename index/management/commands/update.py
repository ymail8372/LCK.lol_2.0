from django.core.management.base import BaseCommand

from index.models import Schedule
from index.models import Ranking_23_summer_regular
from index.models import Champion
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import datetime

class Command(BaseCommand):
    help = 'update command!'
    
    def update_schedule(self) :
        ### chrome driver setting
        url = "https://lolesports.com/schedule?leagues=lck"
        
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")
        option.add_argument("--lang=ko_KR")
        
        driver_path = "/Users/kimminseok/Library/Mobile Documents/com~apple~CloudDocs/Desktop/coding/web_driver"
        driver = webdriver.Chrome(driver_path, chrome_options=option)
        
        driver.get(url)
        while True :
            driver.implicitly_wait(5)
            web_source = driver.page_source
            soup_origin = BeautifulSoup(web_source, "html.parser")
            event = soup_origin.find("div", class_="Event")
            if event != None :
                break
        
        ### quit driver
        driver.quit()
        
        event_tags = event.find_all("div")
        
        ### schedule_objects
        schedule_objects = Schedule.objects.all()
        
        
        for event_tag in event_tags :
            if event_tag['class'][0] == "EventDate" :
                monthday = event_tag.find("span", class_="monthday")
            
                year = 2023 # 이 부분 생각 필요
                month = monthday.text.split('월')[0]
                day_temp1 = monthday.text.split(' ')[1]
                day = day_temp1[:-1]
                weekday_datetime = datetime.date(year, int(month), int(day)).weekday()
                days = ['월', '화', '수', '목', '금', '토', '일']
                weekday = days[weekday_datetime]
            
            elif event_tag['class'][0] == "EventMatch" :
                # break if the Match is about live
                a = event_tag.find("a")
                if a != None :
                    if a['href'].find("live") != -1 :
                        continue
                
                # EventTime
                EventTime = event_tag.find("div", class_="EventTime")

                hour = EventTime.find("span", class_="hour")
                min = EventTime.find("span", class_="minute")
                if min == None :
                    min = 0
                else :
                    min = min.text
                ampm = EventTime.find("span", class_="ampm")

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
                
                if year == 2023 and int(month) >= 6 :
                    etc = "LCK summer 정규시즌 1라운드"
                else :
                    etc = "LCK spring"
                    
                ### update schedule DB
                Schedule.objects.get_or_create(year=year, month=month, day=day, weekday=weekday, team1_name=team1_name, team2_name=team2_name, team1_tricode=team1_tricode.text, team2_tricode=team2_tricode.text, team1_score=team1_score, team2_score=team2_score, hour=hour.text, min=min, ampm=ampm.text, etc=etc)
                
    def update_champion(self) :
        url = "https://lol.fandom.com/wiki/LCK/2023_Season/Summer_Season/Picks_and_Bans"
        
        option = webdriver.ChromeOptions()
        option.add_argument("--headless")
        option.add_argument("--lang=ko_KR")
        
        driver_path = "/Users/kimminseok/Library/Mobile Documents/com~apple~CloudDocs/Desktop/coding/web_driver"
        driver = webdriver.Chrome(driver_path, chrome_options=option)
        
        driver.get(url)
        while True :
            driver.implicitly_wait(5)
            web_source = driver.page_source
            soup_origin = BeautifulSoup(web_source, "html.parser")
            table = soup_origin.find("table", class_="wikitable plainlinks hoverable-rows column-show-hide-1")
            if table != None :
                break
        
        driver.quit()
        
        champions = table.find_all("tr")
        champions.pop(0)
        champions.pop(0)
        for champion in champions :
            td = champion.find_all("td")
            
            # update ban
            for i in range(5, 11) :
                champion_object, created = Champion.objects.get_or_create(name=td[i].get("data-c1"))
                
                if not created :
                    champion_object.ban += 1
                    champion_object.save()
                
            for i in range(15, 19) :
                champion_object, created = Champion.objects.get_or_create(name=td[i].get("data-c1"))
                
                if not created :
                    champion_object.ban += 1
                    champion_object.save()
                
            # update pick
            if "pbh-winner" in td[1] :
                # win team
                champion_object, created = Champion.objects.get_or_create(name=td[11].get("data-c1"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.win += 1
                    champion_object.save()
                
                champion_object, created = Champion.objects.get_or_create(name=td[13].get("data-c1"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.win += 1
                    champion_object.save()
                    
                champion_object, created = Champion.objects.get_or_create(name=td[13].get("data-c2"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.win += 1
                    champion_object.save()
                
                champion_object, created = Champion.objects.get_or_create(name=td[20].get("data-c1"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.win += 1
                    champion_object.save()
                
                
                champion_object, created = Champion.objects.get_or_create(name=td[20].get("data-c2"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.win += 1
                    champion_object.save()
                
                # lose team
                champion_object, created = Champion.objects.get_or_create(name=td[12].get("data-c1"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.lose += 1
                    champion_object.save()
                
                champion_object, created = Champion.objects.get_or_create(name=td[12].get("data-c2"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.lose += 1
                    champion_object.save()
                
                champion_object, created = Champion.objects.get_or_create(name=td[14].get("data-c1"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.lose += 1
                    champion_object.save()
                
                champion_object, created = Champion.objects.get_or_create(name=td[19].get("data-c1"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.lose += 1
                    champion_object.save()
                
                champion_object, created = Champion.objects.get_or_create(name=td[21].get("data-c1"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.lose += 1
                    champion_object.save()
            else :
                # lose team
                champion_object, created = Champion.objects.get_or_create(name=td[11].get("data-c1"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.lose += 1
                    champion_object.save()
                
                champion_object, created = Champion.objects.get_or_create(name=td[13].get("data-c1"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.lose += 1
                    champion_object.save()
                    
                champion_object, created = Champion.objects.get_or_create(name=td[13].get("data-c2"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.lose += 1
                    champion_object.save()
                
                champion_object, created = Champion.objects.get_or_create(name=td[20].get("data-c1"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.lose += 1
                    champion_object.save()
                
                
                champion_object, created = Champion.objects.get_or_create(name=td[20].get("data-c2"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.lose += 1
                    champion_object.save()
                
                # win team
                champion_object, created = Champion.objects.get_or_create(name=td[12].get("data-c1"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.win += 1
                    champion_object.save()
                
                champion_object, created = Champion.objects.get_or_create(name=td[12].get("data-c2"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.win += 1
                    champion_object.save()
                
                champion_object, created = Champion.objects.get_or_create(name=td[14].get("data-c1"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.win += 1
                    champion_object.save()
                
                champion_object, created = Champion.objects.get_or_create(name=td[19].get("data-c1"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.win += 1
                    champion_object.save()
                
                champion_object, created = Champion.objects.get_or_create(name=td[21].get("data-c1"))
                
                if not created :
                    champion_object.pick += 1
                    champion_object.win += 1
                    champion_object.save()

    def convert_team_name_23_summer(self, team) :
        if team == "Gen.G" :
            return "젠지"
        elif team == "T1" :
            return "T1"
        elif team == "kt Rolster" :
            return "kt 롤스터"
        elif team == "Hanwha Life Esports" :
            return "한화생명e스포츠"
        elif team == "Dplus Kia" :
            return "디플러스 기아"
        elif team == "Liiv SANDBOX" :
            return "리브 샌드박스"
        elif team == "Kwangdong Freecs" :
            return "광동 프릭스"
        elif team == "OKSavingsBank BRION" :
            return "OK저축은행 브리온"
        elif team == "DRX" :
            return "DRX"
        elif team == "NongShim REDFORCE" :
            return "농심 레드포스"
        elif team == "TBD" :
            return "미정"

    def reset_ranking_23_summer_regular(self) :
        teams = ["T1", "GEN", "HLE", "KDF", "LSB", "NS", "DK", "DRX", "BRO", "KT"]
        
        for name in teams :
            team_object = Ranking_23_summer_regular.objects.get(tricode=name)
            team_object.game_win = 0
            team_object.game_lose = 0
            team_object.set_win = 0
            team_object.set_lose = 0
            
            team_object.save()

    def update_ranking_23_summer_regular(self) :
        self.reset_ranking_23_summer_regular()
        
        schedule_objects = Schedule.objects.all()
        for schedule_object in schedule_objects :
            if "LCK summer 정규시즌" in schedule_object.etc and schedule_object.year == 2023:
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
        self.update_ranking_23_summer_regular()
        self.update_champion()
