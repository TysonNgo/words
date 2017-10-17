from datetime import datetime
from random import randint
from scrapers import Websites
from time import sleep, time
from WordList import WordList
import inspect

def delay():
	sleep(randint(1,3))

def main():
	classes = dict([member for member in inspect.getmembers(Websites, inspect.isclass) if member[1].__module__ == "scrapers.Websites"])
	
	json_path = "words/%s.json"

	for c in classes:
		print("Collecting words from", c)
		start_time = time()
		wordlist = WordList(json_path % (c,))
		scraper = classes[c]()
		for words in scraper.get_words():
			wordlist.append_to_words(words)
			print (datetime.strftime(datetime.now(), "%b %d %H:%M:%S: "), c, words[:5])
			delay()
		print("Collected words from", c, "in", time()-start_time, "seconds")

if __name__ == "__main__":
	main()