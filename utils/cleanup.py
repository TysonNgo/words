from glob import glob
from os import path, sep
from .WordList import WordList
import json
import re


class CleanUp(object):
	def __init__(self, the_json):
		self.words = WordList(the_json).words
		self.initial_word_count = self.get_total_words()
		self.filename = "cleanup"+sep+path.basename(the_json).replace(".json", "_cleanup.json")
		self.indent = 4
 
	def get_total_words(self):
		words = 0
		for c in self.words:
			for word in self.words[c]:
				words += 1
		return words

	def remove_regex_from_words(self, regex, reverse_match=False, debug=False):
		words = []
		removed = 0
		for c in self.words:
			for word in self.words[c]:
				match = re.findall(regex, word) if reverse_match else not re.findall(regex, word)
				if match:
					words.append(word)
				else:
					if debug == True:
						print(word)
					removed += 1
			#if debug == True:
			#	print(words)			
			self.words[c][:] = words
			words[:] = []
		return removed

	def remove_prefixes(self):
		return self.remove_regex_from_words("-$")

	def remove_suffixes(self):
		return self.remove_regex_from_words("^-")

	def remove_non_roman_alphabets(self):
		return self.remove_regex_from_words("^[a-zA-Z-'\.\s]+$", reverse_match=True)

	def remove_abbreviations(self):
		return self.remove_regex_from_words("^[A-Z]+$")

	def remove_multiple_words(self):
		return self.remove_regex_from_words("\s")

	def remove_apostrophes(self):
		return self.remove_regex_from_words("'")

	def remove_periods(self):
		return self.remove_regex_from_words("\.")

	def remove_hyphens(self):
		return self.remove_regex_from_words("-")

	def update(self):
		with open(self.filename, "w") as f:
			json.dump(self.words, f, indent=self.indent)

def clean():
	def print_removed_from(cleanup):
		def print_removed(to_remove):
			removed = getattr(cleanup, "remove_"+to_remove)()
			print("Removed", removed, "words with", to_remove.replace("_"," "))
		return print_removed

	filenames = glob("words/*.json")

	for filename in filenames:
		cleanup = CleanUp(filename)
		remove = print_removed_from(cleanup)
		print("Cleaning up", filename)

		remove("prefixes")
		remove("suffixes")
		remove("abbreviations")
		remove("apostrophes")
		remove("periods")
		remove("non_roman_alphabets")
		remove("multiple_words")
		remove("hyphens")
		print("Remaining word count:\t", cleanup.get_total_words())
		print("Total word count:\t", cleanup.initial_word_count)
		
		print ("Writing new JSON to", cleanup.filename)
		cleanup.update()


if __name__ == "__main__":
	clean()
