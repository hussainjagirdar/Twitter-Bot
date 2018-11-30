import tarfile
import json
import gzip
import os

class DataLoader(object):
	
	def __init__(self):
		self.DIR = "../data/"
		self.FILE = "database.txt"

	def load_data(self):
		main_filename = self.DIR + "json.gold.tar.gz"
		tar = tarfile.open(main_filename)
		tweetFile = open(self.DIR+self.FILE,"a+")
		i = 1
		for member in tar.getmembers():
			print i
			i = i + 1
			tar.extract(member,path=self.DIR)
			temp_file = self.DIR + member.name
			with gzip.open(temp_file, "rb") as f:
				lines = f.readlines()
				for line in lines:
					d = json.loads(line.decode("utf-8"))
					tweetFile.write(d["text"].encode("utf-8"))
					tweetFile.write("\n")
			os.remove(temp_file)
		tar.close()
		tweetFile.close()

dataLoadIntance = DataLoader()
dataLoadIntance.load_data()
