from bs4 import BeautifulSoup
from time import sleep
import json
import requests
import re

base = "https://en.wikipedia.org"

def random_wiki_article():
	url = base+"/wiki/Special:Random"
	#url = "https://en.wikipedia.org/wiki/Carposina_telesia"
	return requests.get(url)

def get_wiki_links(html: str):
	urls = set()
	for url in re.findall('"(/wiki/.*?)"', html):
		if ":" not in url:
			urls |= set([url])
	return urls

def get_words(html: str):
	soup = BeautifulSoup(html, "html.parser")

	result = ""
	for p in soup.find_all("p"):
		result = " ".join([result, p.text])
	return [w.strip(".,!?<>()[]{}\"';:*") for w in result.split() if re.match("^[a-z]+$", w)]

def write_words():
	with open("words.json") as f:
		words = set(json.load(f).keys())
	with open("words.txt", "w") as f:
		f.write("\n".join(sorted(list(words))))

def main():
	try:
		with open("words.json") as f:
			words = json.load(f) or {}
	except: words = {}

	try:
		with open("visited.json") as f:
			visited = json.load(f) or {}
	except: visited = {}

	articles = 0
	article = random_wiki_article()
	links = set()

	while True:
		sleep(0.5)

		wiki = re.findall("/wiki/.*", article.url)[0]
		if wiki in visited:
			if not links:
				break
			article = requests.get(base+links.pop())
			continue
		else:
			visited[wiki] = ""

		html = article.content.decode("utf-8")
		
		links |= get_wiki_links(html)

		for word in get_words(html):
			if word in words:
				words[word] += 1
			else:
				words[word] = 1

		print(articles,"Getting words from %s" % (article.url,))

		if articles % 10 == 0:
			with open("words.json", "w") as f:
				json.dump(words, f, indent=2)
			with open("visited.json", "w") as f:
				json.dump(visited, f, indent=2)

		articles += 1

if __name__ == "__main__":
	main()
	#write_words()

