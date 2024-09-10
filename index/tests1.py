import os

print(os.getcwd())

for root, dirs, files in os.walk("./index/static/img/teams/") :
	for dir in dirs :
		if "LCK" in dir :
			newname = dir.split(" ")[0] + " " + dir.split(" ")[2]
			os.rename(f"{root}/{dir}", f"{root}/{newname}")		
		elif "Worlds" in dir :
			os.rename(f"{root}/{dir}", f"{root}/Worlds")
