from uuid import uuid1
import json
import os
import re
import urllib2

class Words():
	def __init__(self, out_dir="intermediate_jsons"):
		self.out = out_dir+os.sep+str(uuid1())+".json"
		self.words = {} # frequency counter

	def add_words(self, filename):
		"""adds words from filename (file in wikiextractor/extracted)
		word frequency dict
		"""
		if not os.path.isfile(filename):
			return

		with open(filename) as f:
			words = re.split("\W+", f.read())

		for w in words:
			w = w.strip(".,!?<>()[]{}\"';:*")
			if re.match("^[a-z]+$", w):
				if w in self.words:
					self.words[w] += 1
				else:
					self.words[w] = 1

		with open(self.out, "w") as f:
			json.dump(self.words, f)


class WordQueue():
	with open("./config.json") as f:
		port = json.load(f)["port"]

	@staticmethod
	def get_filename(route='/'):
		"""gets a filename of a file in wikiextractor/extracted
		from a node.js server (index.js)
		"""
		res = None
		try: res = urllib2.urlopen('http://localhost:'+str(WordQueue.port)+route)
		except: pass # this block executes on 404

		if res:
			return json.loads(res.read())["filename"]
