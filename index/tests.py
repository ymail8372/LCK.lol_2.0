from django.test import TestCase
from mwrogue.esports_client import EsportsClient
from datetime import datetime, timedelta

# Create your tests here.



site = EsportsClient("lol")
region = "Korea"
league = "LCK 2024 spring"


response = site.cargo_client.query(
	tables="Tournaments=T, MatchSchedule=MS",
	join_on="T.OverviewPage=MS.OverviewPage",
	where=f"T.Name LIKE '%{league}%'",
	order_by="MS.DateTime_UTC",
	limit=400,
	
	fields="T.Name, MS.Team1, MS.Team2, MS.Team1Score, MS.Team2Score, MS.DateTime_UTC, MS.MVP, MS.MVPPoints",
)

for i in response :
	print(i)
