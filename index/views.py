from django.shortcuts import render
from django.http import JsonResponse
from .models import Schedule
from .models import Ranking_23_spring_regular
from .models import Ranking_23_summer_regular
from selenium import webdriver
from bs4 import BeautifulSoup
import time

def update_schedule() :
    ### chrome driver setting
    url = "https://lolesports.com/schedule?leagues=lck"
    
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    option.add_argument("--lang=ko_KR")
    
    driver_path = "/Users/kimminseok/Library/Mobile Documents/com~apple~CloudDocs/Desktop/coding/web_driver"
    driver = webdriver.Chrome(driver_path, chrome_options=option)
    
    driver.get(url)
    driver.implicitly_wait(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
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
            if a != None :
                if a['href'].find("live") != -1 :
                    break
            
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
            team1_name = convert_team_name_23_summer(team1_name)
            team1_tricode = team1.find("span", class_="tricode")
            
            team2 = teams_tag.find("div", class_="team2")
            team2_name = team2.find("span", class_="name").text
            team2_name = convert_team_name_23_summer(team2_name)
            team2_tricode = team2.find("span", class_="tricode")
            
            if teams_tag.find("div", class_="score") != None :
                score = teams_tag.find("div", class_="score")
                scoreTeam1 = score.find("span", class_="scoreTeam1").text
                scoreTeam2 = score.find("span", class_="scoreTeam2").text
            else :
                scoreTeam1 = 0
                scoreTeam2 = 0
            
            etc = "LCK summer 정규시즌 1라운드"
            
            ### update schedule DB
            # check the schedule already exist in schedule DB
            check_db = 0
            for schedule_object in schedule_objects :
                if schedule_object.year == year and schedule_object.month == int(month) and schedule_object.day == int(day) and schedule_object.hour == int(hour.text) :
                    check_db = 1
                    break
            
            # if there is no schedule in schedule DB
            if check_db == 0 :
                Schedule(year=year, month=month, day=day, weekday=weekday, team1_name=team1_name, team2_name=team2_name, team1_tricode=team1_tricode.text, team2_tricode=team2_tricode.text, team1_score=scoreTeam1, team2_score=scoreTeam2, hour=hour.text, min=min, ampm=ampm.text, etc=etc).save()

def convert_team_name_23_summer(team) :
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

def reset_ranking_23_summer_regular() :
    Ranking_23_summer_regular.objects.all().delete()
    
    Ranking_23_summer_regular(name="T1", tricode="T1").save()
    Ranking_23_summer_regular(name="젠지", tricode="GEN").save()
    Ranking_23_summer_regular(name="한화생명e스포츠", tricode="HLE").save()
    Ranking_23_summer_regular(name="광동 프릭스", tricode="KDF").save()
    Ranking_23_summer_regular(name="리브 샌드박스", tricode="LSB").save()
    Ranking_23_summer_regular(name="농심 레드포스", tricode="NS").save()
    Ranking_23_summer_regular(name="디플러스 기아", tricode="DK").save()
    Ranking_23_summer_regular(name="DRX", tricode="DRX").save()
    Ranking_23_summer_regular(name="OK저축은행 브리온", tricode="BRO").save()
    Ranking_23_summer_regular(name="kt 롤스터", tricode="KT").save()

def update_ranking_23_summer_regular() :
    reset_ranking_23_summer_regular()
    
    schedule_objects = Schedule.objects.all()
    for schedule_object in schedule_objects :
        if "LCK summer 정규시즌" in schedule_object.etc and schedule_object.year == 2023:
            team1 = Ranking_23_spring_regular.objects.get(name=schedule_object.team1_name)
            team2 = Ranking_23_spring_regular.objects.get(name=schedule_object.team2_name)
            
            # when the schedule is not started yet
            if schedule_object.team1_score == 0 and schedule_object.team2_score == 0 :
                break
            
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

#def reset_ranking_23_spring_regular() :
#    Ranking_23_spring_regular.objects.all().delete()
    
#    Ranking_23_spring_regular(name="T1", tricode="T1").save()
#    Ranking_23_spring_regular(name="젠지", tricode="GEN").save()
#    Ranking_23_spring_regular(name="한화생명e스포츠", tricode="HLE").save()
#    Ranking_23_spring_regular(name="광동 프릭스", tricode="KDF").save()
#    Ranking_23_spring_regular(name="리브 샌드박스", tricode="LSB").save()
#    Ranking_23_spring_regular(name="농심 레드포스", tricode="NS").save()
#    Ranking_23_spring_regular(name="디플러스 기아", tricode="DK").save()
#    Ranking_23_spring_regular(name="DRX", tricode="DRX").save()
#    Ranking_23_spring_regular(name="프레딧 브리온", tricode="BRO").save()
#    Ranking_23_spring_regular(name="kt 롤스터", tricode="KT").save()

#def update_ranking_23_spring_regular() :
#    reset_ranking_23_spring_regular()
    
#    schedule_objects = Schedule.objects.all()
#    for schedule_object in schedule_objects :
#        if "LCK spring 정규시즌" in schedule_object.etc and schedule_object.year == 2023:
#            team1 = Ranking_23_spring_regular.objects.get(name=schedule_object.team1_name)
#            team2 = Ranking_23_spring_regular.objects.get(name=schedule_object.team2_name)
            
#            # update game_win, game_lose
#            if schedule_object.team1_score > schedule_object.team2_score :
#                team1.game_win += 1
#                team2.game_lose += 1
#            else :
#                team1.game_lose += 1
#                team2.game_win += 1
            
#            # update set_win, set_lose
#            team1.set_win += schedule_object.team1_score
#            team1.set_lose += schedule_object.team2_score
#            team2.set_win += schedule_object.team2_score
#            team2.set_lose += schedule_object.team1_score
        
#            # apply update
#            team1.save()
#            team2.save()

# response Json to JS
def get_schedules(request) :
    schedule_values = Schedule.objects.values()
    
    return JsonResponse(list(schedule_values), safe=False)

def index(request) :
    update_schedule()
    #update_ranking_23_spring_regular()
    update_ranking_23_summer_regular()
    
    schedules = Schedule.objects.all()
    
    return render(request, 'index.html', {"schedules": schedules})
