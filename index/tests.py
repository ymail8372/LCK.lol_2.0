import os

print(os.getcwd())

for root, dirs, files in os.walk("./index/templates/history_contents") :
	for file in files :
		if file[0] == "." :
			continue
		
		if "Worlds" in root:
			print("file : ", f"{root}/{file}")
			
			with open(f"{root}/{file}", "r") as read_file :
				year = file.split(".")[0]
				content = read_file.read()
				content = content.replace(f"Worlds 20{year}", f"20{year}/Worlds")
			
			with open(f"{root}/{file}", "w") as write_file :
				print("write : ", f"{root}/{file}")
				write_file.write(content)
			

		
