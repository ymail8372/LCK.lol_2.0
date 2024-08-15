import os

print(os.getcwd())

for root, dirs, files in os.walk("./index/templates/history_contents/") :
	for file in files :
		if file[0] == "." :
			continue
		print("file : ", file)
		with open(f"{root}/{file}", "r") as read_file :
			content = read_file.read()
			content = content.replace("Top_blcak.webp", "Top_black.webp")
		
		with open(f"{root}/{file}", "w") as write_file :
			print("write : ", f"{root}/{file}")
			write_file.write(content)
			

		
