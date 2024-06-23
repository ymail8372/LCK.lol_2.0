import os
import re

root_dir = "/Users/kimminseok/Library/Mobile Documents/com~apple~CloudDocs/Desktop/coding/LCKlol/index/templates/history_contents"
old_word = "MID.webp"
new_word = "Mid.webp"

for dirpath, dirnames, filenames in os.walk(root_dir) :
	for filename in filenames :
		if ".html" in filename :
			filepath = os.path.join(dirpath, filename)
			with open(filepath, "r", encoding="utf-8") as file :
				content = file.read()
				content = re.sub(old_word, new_word, content)
			with open(filepath, "w", encoding="utf-8") as file :
				file.write(content)
				