from PyPDF2 import PdfFileReader
from glob import glob
from os import sep
import json
import re

def remove_punctuation(s: str):
    """Removes punctuation from a word s
    """
    return s.strip(".,!?<>()[]{}\"';:*")

def is_word(s: str):
    """Checks if a "word" is all lowercase
    """
    return re.match("^[a-z]+$", s)

def write_words():
    jsons = glob("word_frequencies/*.json")
    words = set()
    for j in jsons:
        with open(j) as f:
            words |= set(json.load(f).keys())
    with open("words.txt", "w") as f:
        f.write("\n".join(sorted(list(words))))

def main():
    pdfs = glob("ebooks/**/*.pdf", recursive=True)
    words = {}

    for pdf in pdfs:
        print("Retrieving words from %s" % (pdf,))
        with open(pdf, "rb") as f:
            pdf_reader = PdfFileReader(f)
            num_pages = pdf_reader.numPages

            for p in range(num_pages):
                page = pdf_reader.getPage(p)
                text = page.extractText().split()

                for word in text:
                    word = remove_punctuation(word)
                    if not is_word(word):
                        print("NOT A WORD", word)
                        continue

                    print(word)
                    if word in words:
                        words[word] += 1
                    else:
                        words[word] = 1

                print("Finished checking page", p+1, text[:5])

        with open("word_frequencies"+sep+pdf.split(sep)[-1].replace(".pdf", ".json"), "w") as f:
            json.dump(words, f, indent=2)
            words.clear()


if __name__ == "__main__":
    main()
    write_words()