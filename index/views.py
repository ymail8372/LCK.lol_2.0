from django.shortcuts import render
from .models import Version
from .models import Schedule
from requests import get
from selenium import webdriver
from bs4 import BeautifulSoup
import time
    
# Create your views here.
def get_schedule() :
    # chrome driver setting
    url = "https://lolesports.com/schedule?leagues=lck"
    
    option = webdriver.ChromeOptions()
    option.add_argument("--headless")
    
    driver_path = "/Users/kimminseok/Library/Mobile Documents/com~apple~CloudDocs/Desktop/coding/web_driver"
    driver = webdriver.Chrome(driver_path, chrome_options=option)
    
    driver.get(url)
    time.sleep(1)
    web_source = driver.page_source
    
    # schedule
    schedule = []
    
    # extract web source using Beautifulsoup
    soup_origin = BeautifulSoup(web_source, "html.parser")
    #date = soup_origin.find_all("div", class_="EventDate")
    match = soup_origin.find_all("div", class_="EventMatch")
    
    # EventMatch
    for i in match :
        # break if the Match is about live
        a = i.find("a")
        print(a['href'])
        if a['href'].find("live") != -1 :
            break
        
        teams = i.find("div", class_="teams")
        
        team1 = teams.find("div", class_="team1")
        team1_name = team1.find("span", class_="name")
        team2 = teams.find("div", class_="team2")
        team2_name = team2.find("span", class_="name")
        
        score = teams.find("div", class_="score")
        scoreTeam1 = score.find("span", class_="scoreTeam1")
        scoreTeam2 = score.find("span", class_="scoreTeam2")
        
        schedule.append([team1_name.text, team2_name.text, scoreTeam1.text, scoreTeam2.text])
    
    print(schedule)
    
    # EventMatch
    
    driver.quit()

def index(request) :
    get_schedule()
    
    version = Version.objects.all()
    schedule = Schedule.objects.all()
    
    return render(request, 'index.html', {"versions": version, "schedules": schedule})
