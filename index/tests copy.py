from mwrogue.esports_client import EsportsClient
import models

site = EsportsClient("lol")

players = site.cargo_client.query(
	tables="Players=P",
	where=f"P.Country = South Korea",
	limit=400,
	
	fields="P.Name, P.NativeName, P.Role",
)

print(players)