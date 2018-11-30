import re
DIR = "../data/"
FILE = "database.txt"
NEW_FILE = "preprocessed.txt"
NEW_NEW_FILE = "final_data.txt"

#Removing unneccesary url and lines.
old_file = open(DIR+FILE,"r")
new_file = open(DIR+NEW_FILE,"a+")
lines = old_file.readlines()
for line in lines:
	if(line == "\n"):
		continue
	else:
		line = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','',line,flags=re.MULTILINE)
		if(line != "\n"):
			new_file.write(line)
old_file.close()
new_file.close()


#Retrieving only valid lines (English)
new_file = open(DIR+NEW_FILE,"r")
new_new_file = open(DIR+NEW_NEW_FILE,"a+")
lines = new_file.readlines()
for line in lines:
	try:
		line.encode(encoding='utf-8').decode('ascii')
	except UnicodeDecodeError:
		continue
	else:
		new_new_file.write(line)
new_file.close()
new_new_file.close()
