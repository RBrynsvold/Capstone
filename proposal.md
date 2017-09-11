
# Project Proposal: Literary Analysis with NLP in collaboration with Terminal Labs

__Goal__: Gain some insight about literary texts using NLP.  I haven't settled yet on the exact analysis I want to do, but my candidate ideas are:
* __Networks from Topic models__
  * Develop a topic model of some subset of the Gutenberg corpus, and use that network to create a network of the texts.
  * I am interested in applications where you can create a topic model from an existing corpus, and then use that
  model to suggest/display similar documents from the corpus when a document is added
  * I believe this has applications in various knowledge management systems - specifically to my top target company and their knowledge management and bug tracking products.
  
* Backup/auxilliary topic: authorship of books, based on other works by that author (training set = one set of his/her
  books, test set = another set)

Other
* How language changes over time
* How words have changed meaning over time
* Evolution of slang
* Character sentiment analysis: choose some subset of famous literary characters and analyze their dialogue
  to do sentiment analysis... challenge here would be to isolate a given character's dialogue, so not sure
  this is actually feasible.

Lexicon Valley

__Data Source__: [Project Gutenberg](http://www.gutenberg.org/wiki/Gutenberg:Information_About_Robot_Access_to_our_Pages) has full text of 54,000 (!!) public domain books available for download!  This will be a really great dataset to use to play with NLP.

__Presentation Format__: Slides

__9/8 updates__: Last weekend I did some initial investigation of how to get the data.  Although I haven't yet downloaded/accessed it, I am 100% sure that I can get it - I found lots of pages where people detail how they went about downloading it.  I even saw some pre-existing libraries for working with this specific dataset (parsing the strings, etc).

__Next steps__: NLP Literary Analysis/'Digitial Humanities' research.  This is a new field of course, but from what I can tell, it's already pretty rich.  I'm still liking my authorship prediction and/or latent feature analysis for thematic elements, and with some research this weekend on what kinds of things people are doing and having success with, I think I will be ready to have a firm subject proposal by middle/end of next week.


### Terminal Labs collaboration

My [Terminal Labs](https://terminallabs.com/) contact (Michael Verhulst, CIO) and I have tentatively agreed to go ahead with a collaboration on my NLP project.  

Their interest in the project is use of and exposure for their open-source [project Rambo](https://github.com/terminal-labs/rambo).  From the project github:

>This repo is for provisioning and configuration of virtual machines (and containers) in a simple and predictable way. Just run one command and your vms is up, code is deployed and your app is running, on any supported platform.

>At this time the repo allows you to create a debian 8 Jessie VM on multiple providers (AWS EC2, Digitalocean, Virtualbox, lxc) The base machine configuration is a debian 8 Jessie 64bit os with 1024mb ram, and 30GB drive.

Terminal Labs is a local consultancy that specializes in Python, Data Science, and general DevOps/server stuff.  In the conversation I had the Michael today, we discussed Terminal Labs work in reproducibility and persistence of data science work, so what I think I will get out of this collaboration - in addition to Austin Tech community exposure and technical mentorship - is a greater technical depth of the project, that I anticipate would be interesting to very technical data science professionals and hiring managers.

They have also asked me to submit a talk for presentation at the [PyTexas conference](https://www.pytexas.org/2017/) on Nov 18th and 19th.

Next step with them: We'll be meeting next week to get started.  I'll be presenting a more fleshed-out project proposal, and they will be familiarizing me with the tools that I will be using.  Michael has committed to spend 12-15hrs with me next week to get the project off the ground.
