const PORT = require('./config').port || 3000;
const express = require('express');
const app = express();

const glob = require('glob');
const wikiextractorOutPath = require('./config').wikiextractorOutPath;

var files = getFiles();
var visited = new Set();

function getFiles(popLast=true){
	let files = glob.sync(wikiextractorOutPath+'/**/wiki_*')
	if (popLast){
		files.pop(); // the last file will be open for writing by WikiExtractor.py
	}
	return files;
}

app.get('/', (req, res) => {
	let file = files.pop();
	while (visited.has(file)){
		file = files.pop();
	}
	if (file){
		res.json({'filename': file});
		visited.add(file);
	} else {
		res.sendStatus(404);
		files = getFiles();
	}
})

// this is hacky since '/' will eventually return all 
// but 1 wiki_* file because the most recent file
// is being used by WikiExtractor. so to avoid having
// main.py read that file, '/' excludes the most recent file
// when WikiExtractor finishes running, the last file path can
// be obtained from this endpoint
app.get('/remaining', (req, res) => {
	let files = getFiles(false);
	if (files.length === 1){
		res.json({'filename': files[0]});
	} else {
		res.redirect('/');
	}
})

app.listen(PORT, () => console.log(`app listening on port ${PORT}`))