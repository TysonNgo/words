import requests


class ScrapeWords(object):
	def __init__(self, base_url):
		if not ("!letter!" in base_url and "!page!" in base_url):
			message = (
			"base_url must contain:\n"
			"  !letter!\n"
			"  !page!\n\n"
			"An example is: http://www.dictionary.com/list/!letter!/!page!")
			raise Exception(message)

		self.url = base_url

	def get_response(self, url):
		res = None
		while not res:
			try:
				res = requests.get(url)
			except Exception as ex:
				print(ex)
		return res

	def get_pages(self):
		a = ord("a")
		z = ord("z")
		for i in range(z-a+1):
			letter = chr(a+i)
			page = 1

			res = self.get_response(self.url.replace("!letter!",letter).replace("!page!",str(page)))
			last_page = self.scrape_last_page_number(res.content)
			
			while page <= last_page:
				yield res.content
				page += 1
				res = self.get_response(self.url.replace("!letter!",letter).replace("!page!",str(page)))

	def get_words(self):
		for page in self.get_pages():
			yield self.scrape_words_from(page)

	def scrape_last_page_number(self, html):
		"""override this method, return int"""

	def scrape_words_from(self, html):
		"""override this method, return list of words ["a", "aa", "aaa"]"""
