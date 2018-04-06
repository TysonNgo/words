#!/bin/bash
if [ $# -ne 1 ]; then
	echo
	echo "Usage: ./run.sh <wikidump>"
	echo
	echo "    where <wikidump> is a path to an XML file"
	echo "    of a Wikipedia dump"
	echo
	echo "Download zipped XML file from https://meta.wikimedia.org/wiki/Data_dump_torrents#English_Wikipedia"
	exit 1
fi

if ! { [ -d "wikiextractor" ] && [ -f "wikiextractor/WikiExtractor.py" ]; }; then
	echo
	echo "Missing: wikiextractor/WikiExtractor.py"
	git clone https://github.com/attardi/wikiextractor.git
fi

wikiextractor="wikiextractor/WikiExtractor.py"
options="-b 500K -o extracted"

python $wikiextractor $1 $options > wikiextractor.log 2>&1 &
sleep 10
node index.js > server.log 2>&1 &
sleep 10
python main.py > words.log 2>&1 &

tail -f words.log
