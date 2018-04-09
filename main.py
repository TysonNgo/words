from functools import reduce
from glob import glob
from pathlib import Path
import json
import requests

words_json = "words.json"
d_com_json = "DictionaryCom_cleanup.json"
mw_com_json = "MerriamWebsterCom_cleanup.json"

def download_jsons():
	words_repo = "https://raw.githubusercontent.com/TysonNgo/words/"

	jsons = {
		"wiki/": [
			words_json
		],
		"dictionary/cleanup/": [
			d_com_json,
			mw_com_json
		]
	}

	for branch in jsons:
		for JSON in jsons[branch]:
			if not Path(JSON).is_file():
				url = words_repo+branch+JSON
				print("Downloading", JSON, "from", url)
				with open(JSON, "w") as f:
					json.dump(requests.get(url).json(), f)

def cleanup(words: set):
	for filename in glob("manual_word_removal/*char.txt"):
		with open(filename) as f:
			WORDS = f.read().split("\n")

		for w in WORDS:
			try: words.remove(w)
			except: pass

def main():
	download_jsons()

	with open(words_json) as f: words = json.load(f)
	with open(d_com_json) as f: d_com = json.load(f)
	with open(mw_com_json) as f: mw_com = json.load(f)

	# convert above jsons to word sets
	words = set(filter(lambda k: words[k] > 1, words.keys()))
	d_com = set(reduce(lambda x, y: x+y, d_com.values()))
	mw_com = set(reduce(lambda x, y: x+y, mw_com.values()))

	fin_set = (mw_com | d_com) & words

	cleanup(fin_set)

	with open("words.txt", "w") as f:
		f.write("\n".join(sorted(
			list(fin_set),
		key=lambda x: len(x))))

if __name__ == "__main__":
	main()
