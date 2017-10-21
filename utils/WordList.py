from os.path import isfile
import json
import re


class WordList(object):
	"""This class creates and modifies JSON files that contain word lists"""
	def __init__(self, json_filename, indent=4):
		self.indent = indent
		self.filename = json_filename
		if isfile(self.filename):
			with open(self.filename) as f:
				self.words = json.load(f)
		else:
			self.words = self.__get_empty_abc_dict()

			with open(self.filename, "w") as f:
				json.dump(self.words, f, indent=self.indent)

	def __get_empty_abc_dict(self):
		words = {}
		a = ord("a")
		z = ord("z")
		for i in range(z-a+1):
			c = chr(a+i)
			words[c] = []
		return words

	def append_to_words(self, words):
		"""words is one of:
		- a dict of (key, value) pair ("a"-"z", [str, ...])
		- a list of str"""
		if isinstance(words, type([])):
			word_dict = self.__get_empty_abc_dict()
			for word in words:
				if len(word) > 0:
					try:
						word_dict[word[0].lower()].append(word)
					except KeyError as e:
						print(word+" is not a valid word")
		elif isinstance(words, type({})):
			word_dict = words

		for letter in word_dict:
			# validate key
			if not re.findall("^[a-z]$", letter):
				raise Exception(letter+" is not a letter from a to z")

			word_list = set(self.words[letter])

			for word in word_dict[letter]:
				# validate value
				if word[0].lower() != letter:
					raise Exception(word+" does not start with the letter "+letter)
				word_list.add(word)
		
			self.words[letter][:] = sorted(list(word_list))

		with open(self.filename, "w") as f:
			json.dump(self.words, f, indent=self.indent)
