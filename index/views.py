from django.shortcuts import render
from .models import Schedule
from .models import Ranking_23_spring_regular
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Team class
class Team :
    def __init__(self, name, tricode, game_win=0, game_lose=0, set_win=0, set_lose=0, etc=" - ") :
        self.name = name
        self.tricode = tricode
        self.game_win = game_win
        self.game_lose = game_lose
        self.set_win = set_win
        self.set_lose = set_lose
        self.etc = etc
    
def reset_ranking_23_spring_regular() :
    Ranking_23_spring_regular.objects.all().delete()
    init_ranking_23_spring_regular()
    
def init_ranking_23_spring_regular() :
    Ranking_23_spring_regular(name="T1", tricode="T1").save()
    Ranking_23_spring_regular(name="Gen.G", tricode="GEN").save()
    Ranking_23_spring_regular(name="Hanwha Life Esports", tricode="HLE").save()
    Ranking_23_spring_regular(name="Kwangdong Freecs", tricode="KDF").save()
    Ranking_23_spring_regular(name="Liiv SANDBOX", tricode="LSB").save()
    Ranking_23_spring_regular(name="NongShim REDFORCE", tricode="NS").save()
    Ranking_23_spring_regular(name="Dplus Kia", tricode="DK").save()
    Ranking_23_spring_regular(name="DRX", tricode="DRX").save()
    Ranking_23_spring_regular(name="BRION", tricode="BRO").save()
    Ranking_23_spring_regular(name="kt Rolster", tricode="KT").save()

def update_schedule() :
    ### chrome driver setting
    url = "https://lolesports.com/schedule?leagues=lck"
    
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    
    driver_path = "/Users/kimminseok/Library/Mobile Documents/com~apple~CloudDocs/Desktop/coding/web_driver"
    driver = webdriver.Chrome(driver_path, chrome_options=option)
    
    driver.get(url)
    #driver.execute_script("window.scrollTo(0,0);")
    time.sleep(1)
    web_source = driver.page_source
    
    ### quit driver
    driver.quit()
    
    ### schedule_objects
    schedule_objects = Schedule.objects.all()
    
    ### extract web source using Beautifulsoup
    soup_origin = BeautifulSoup(web_source, "html.parser")
    
    event = soup_origin.find("div", class_="Event")
    event_tags = event.find_all("div")
    
    for event_tag in event_tags :
        if event_tag['class'][0] == "EventDate" :
            weekday = event_tag.find("span", class_="weekday")
            monthday = event_tag.find("span", class_="monthday")
        
            year = 2023 # 이 부분 생각 필요
            month = monthday.text.split('월')[0]
            day_temp1 = monthday.text.split(' ')[1]
            day = day_temp1[:-1]
            weekday = weekday.text[0]
        
        elif event_tag['class'][0] == "EventMatch" :
            # break if the Match is about live
            a = event_tag.find("a")
            if a['href'].find("live") != -1 :
                break
            
            # EventTime
            EventTime = event_tag.find("div", class_="EventTime")

            hour = EventTime.find("span", class_="hour")
            min = EventTime.find("span", class_="minute")
            ampm = EventTime.find("span", class_="ampm")

            #EventTeam
            teams_tag = event_tag.find("div", class_="teams")
                
            team1 = teams_tag.find("div", class_="team1")
            team1_name = team1.find("span", class_="name")
            team2 = teams_tag.find("div", class_="team2")
            team2_name = team2.find("span", class_="name")
            
            score = teams_tag.find("div", class_="score")
            scoreTeam1 = score.find("span", class_="scoreTeam1")
            scoreTeam2 = score.find("span", class_="scoreTeam2")
            
            ### update schedule DB
            check_db = 0
            for schedule_object in schedule_objects :
                if schedule_object.year == year and schedule_object.month == int(month) and schedule_object.day == int(day) and schedule_object.hour == int(hour.text) :
                    check_db = 1
                    break
            
            # if there is no schedule in DB
            if check_db == 0 :
                if min == None :
                    Schedule(year=year, month=month, day=day, weekday=weekday, team1_name=team1_name.text, team2_name=team2_name.text, team1_score=scoreTeam1.text, team2_score=scoreTeam2.text, hour=hour.text, min=0, ampm=ampm.text).save()
                else :
                    Schedule(year=year, month=month, day=day, weekday=weekday, team1_name=team1_name.text, team2_name=team2_name.text, team1_score=scoreTeam1.text, team2_score=scoreTeam2.text, hour=hour.text, min=min.text, ampm=ampm.text).save()
            
def update_ranking_23_spring_regular() :
    reset_ranking_23_spring_regular()
    
    schedule_objects = Schedule.objects.all()
    for schedule_object in schedule_objects :
        if "23_spring_regular" in schedule_object.etc:
            team1 = Ranking_23_spring_regular.objects.get(name=schedule_object.team1_name)
            team2 = Ranking_23_spring_regular.objects.get(name=schedule_object.team2_name)
            
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

def index(request) :
    #init_ranking_23_spring_regular()
    update_schedule()
    update_ranking_23_spring_regular()
    
    schedule = Schedule.objects.all()
    
    return render(request, 'index.html', {"schedules": schedule})
