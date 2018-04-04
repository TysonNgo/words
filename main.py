from bs4 import BeautifulSoup
from time import sleep
import json
import requests
import re

def random_wiki_article():
	url = "https://en.wikipedia.org/wiki/Special:Random"
	#url = "https://en.wikipedia.org/wiki/Carposina_telesia"
	return requests.get(url)

def get_wiki_links(html: str, visited: set):
	urls = []
	for url in re.findall('"(/wiki/.*?)"', html):
		if ":" not in url and url not in visited:
			urls.append(url)
			visited |= set([url])
	return urls

def get_words(html: str):
	soup = BeautifulSoup(html, "html.parser")

	result = ""
	for p in soup.find_all("p"):
		result = " ".join([result, p.text])
	return [w.strip(".,!?<>()[]{}\"';:*") for w in result.split() if re.match("^[a-z]+$", w)]

def write_words():
	with open("words.txt") as f:
		words = set(f.read().splitlines())
	with open("words.json") as f:
		words = set(json.load(f).keys())
	with open("words.txt", "w") as f:
		f.write("\n".join(sorted(list(words))))

def main():
	words = {}

	articles = 300
	article = random_wiki_article()
	visited = set(re.findall("/wiki/.*", article.url))
	links = []

	while articles > 0:
		html = article.content.decode("utf-8")
		if len(visited) < articles:
			links += get_wiki_links(html, visited)

		for word in get_words(html):
			if word in words:
				words[word] += 1
			else:
				words[word] = 1

		url = "https://en.wikipedia.org"+links.pop()
		article = requests.get(url)

		sleep(0.5)
		print(articles,"Getting words from %s" % (url,))
		articles -= 1

	with open("words.json", "w") as f:
		json.dump(words, f, indent=2)

if __name__ == "__main__":
	main()
	write_words()

