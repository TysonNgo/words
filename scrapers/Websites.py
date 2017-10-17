from bs4 import BeautifulSoup
from .ScrapeWords import ScrapeWords


class DictionaryCom(ScrapeWords):
	def __init__(self):
		super().__init__("https://dictionary.com/list/!letter!/!page!")

	def scrape_last_page_number(self, html):
		soup = BeautifulSoup(html, "html.parser")
		
		last_page = [div for div in soup.find_all("div") if "pagination" in str(div)][-1]
		#result["last_page_url"] = [a for a in last_page.find_all("a") if "Last" in str(a)][0]["href"]
		last_page = max([int(a["href"].split("/")[-1]) for a in last_page.find_all("a")])
		return last_page

	def scrape_words_from(self,html):
		soup = BeautifulSoup(html, "html.parser")
		wordslist = None
		words = []
		for div in soup.find_all("div"):
			try:
				if "words-list" in div["class"]:
					wordslist = div
					break
			except:
				pass

		for span in wordslist.find_all("span"):
			try:
				if "word" in span["class"]:
					words.append(span.text)
			except:
				pass

		return words


class MerriamWebsterCom(ScrapeWords):
	def __init__(self):
		super().__init__("https://www.merriam-webster.com/browse/dictionary/!letter!/!page!")

	def scrape_last_page_number(self, html):
		soup = BeautifulSoup(html, "html.parser")
	
		for span in soup.find_all("span"):
			if "page" in str(span):
				# example text of span tag containing last page number
				# page 1 of 73
				last_page = int(span.text.split(" ")[-1])
		return last_page

	def scrape_words_from(self,html):
		soup = BeautifulSoup(html, "html.parser")
		entries = None
		words = []
		for div in soup.find_all("div"):
			try:
				if "entries" in div["class"]:
					entries = div
					break
			except:
				pass

		for a in entries.find_all("a"):
			words.append(a.text)

		return words
