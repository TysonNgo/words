from glob import glob
from multiprocessing import Pool
from time import sleep
from Words import Words, WordQueue
import json
import os
import sys

def merge_intermediate_jsons():
	words = {}
	for filename in glob("intermediate_jsons/*.json"):
		with open(filename) as f:
			tmp = json.load(f)
		for w in tmp:
			if w in words:
				words[w] += tmp[w]
			else:
				words[w] = tmp[w]

	with open("words.json", "w") as f:
		json.dump(words, f)

def add_words_del(filename, words):
	words.add_words(filename)
	try: os.remove(filename)
	except Exception as ex: print ex

def main():
	consecutive_tries = 0
	words = Words()

	while True:
		filename = WordQueue.get_filename()
		if filename:
			print filename
			add_words_del(filename, words)
			consecutive_tries = 0
			words.add_words(filename)
		else:
			if consecutive_tries > 5:
				return
			consecutive_tries += 1
			sleep(5)


if __name__ == "__main__":
	pool = Pool(5, initializer=main)
	pool.close()
	pool.join()

	sleep(5)
	words = Words()
	filename = WordQueue.get_filename("/remaining")
	print filename
	if filename:
		add_words_del(filename, words)

	merge_intermediate_jsons()
