# words
This project provides a list of English words acquired through various means. Each of these methods for acquiring the words are in separate branches of this repository.

Each list of English words is located in a file called `words.txt` in the root of each branch.

### Branches

`dictionary` - acquires a list of English words by scraping dictionary websites

`book` - acquires a list of English words from ebooks

`wiki` - acquires a list of English words from wikipedia dump (~5 million articles)


### Finalized words.txt

The words.txt in this branch is the finalized version.

The method I used to come up with the final list of "words" is to take words from the `words.json` file in the `wiki` branch that intersect with the two JSONs: `DictionaryCom_cleanup.json` and `MerriamWebsterCom_cleanup.json` from the dictionary branch. Then I proceeded to "manually" delete words in the list that contain 2-3 characters.

This was a necessary step because both dictionary.com and merriam-webster.com contain definitions for more than just "words", such as, abbreviations, slang, and names of places.

### Possible exclusions to include in words.txt

- names (there currently appears to be English names such as alex, robert, christina, etc.)

