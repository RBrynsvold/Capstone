# 9-18 Status Report

## Progress

* Obtained gutenberg-tar data dump  
  * All .txt files
  * 36.7 GB
  * Many layered directories (no clear organizational schema)
  * Multiple languages
* Explored other methods of getting the data programmatically/reproducibly
  * Rsync
  * Gutenberg API
* Test run of loading 3 sample documents (locally)
  * Successfully loaded 1/3 - other three were not in English
  * Used NLTK PlainTextCorpusReader
* NLP/LDA research (articles, Patrick Harrison PyData talk, covering LDA and Word2Vec)
* AWS and Rambo progress
  * Successfully spun up a rambo vm on AWS with my TL sponsor over the weekend

## Challenges --> Next Steps

* tar download includes non-english, and I think no metadata (how to discriminate btwn)
* Records not tagged
  * Next step: figure out way to tag using either meta-data, or text parsing.  This is a big one.
* Documents have 'crud' at beginning and end
  * Next step: figure out how to parse to get only the book text (cut out gutenberg legal stuff, copyright info, etc etc)
* Lots to learn about practically applying NLP, LDA, etc
* Not yet satisfied with data obtaining method
  * Next step: narrow down options, pursue, and time-box.  Have backup in case no programmatic method is working
* Still working out vm/rambo workflow, although I think this is pretty close to resolved
* Python 2.7 or Python 3?

**Need help prioritizing, finalizing data acquisition and parsing method to use for this project**
