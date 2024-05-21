from django.test import TestCase
from mwrogue.esports_client import EsportsClient
from datetime import datetime, timedelta

# Create your tests here.



site = EsportsClient("lol")
region = "Korea"
league = "LCK 2024 spring playoffs"

response = site.cargo_client.query(
	tables="Players=P, MatchScheduleGame=MSG, ScoreboardGames=SG",
	join_on="MSG.MVP=P.ID, MSG.GameId=SG.GameId",
	where=f"SG.Tournament=\"LCK 2024 spring\"",
	limit=400,
	
	fields="SG.DateTime_UTC, P.NativeName, P.Team, P.Role, P.Country, MSG.MVP",
)

for i in response :
	print(i)
