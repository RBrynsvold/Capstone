
# Project Proposal: Networks from Topic Models (working title)
* Develop a topic model of some subset of the Project Gutenberg corpus, and use that model to create a network of the texts. 
   * Specific subset TBD; definitely English-language only, maybe fiction/non-fiction only, may have to reduce if I can't get good topics out of my model
* I am interested in applications where you can create a topic model from an existing corpus, and then use that model to identify similar documents from the training corpus when a new document is added
* I believe this has applications in various knowledge management systems - specifically to my top target company and their knowledge management and bug tracking products.
  
* Backup/auxilliary topic: authorship of books, based on other works by that author (training set = one set of his/her
  books, test set = another set)

__Data Source__: [Project Gutenberg](http://www.gutenberg.org/wiki/Gutenberg:Information_About_Robot_Access_to_our_Pages) has full text of 54,000 (!) public domain books available for download!  This will be a really great dataset to use to play with NLP.

__Next steps__: Further research on topic modeling (LDA - latent dirchlet analysis - etc).

__Notes__ 
* I found lots of pages where people detail how they went about downloading the PG dataset.  
* I've even seen some pre-existing libraries for working with the PG dataset (parsing the strings, etc).


### Terminal Labs collaboration  

My capstone partner, Terminal Labs, has asked me to use their open-source [project Rambo](https://github.com/terminal-labs/rambo).  From the project github:

>This repo is for provisioning and configuration of virtual machines (and containers) in a simple and predictable way. Just run one command and your vms is up, code is deployed and your app is running, on any supported platform.

>At this time the repo allows you to create a debian 8 Jessie VM on multiple providers (AWS EC2, Digitalocean, Virtualbox, lxc) The base machine configuration is a debian 8 Jessie 64bit os with 1024mb ram, and 30GB drive.

By using Rambo, I'll add additional depth to the project around reproducibility and persistence of data science work.  

I'll also be submitting my project as a talk for the [PyTexas conference](https://www.pytexas.org/2017/) on Nov 18th and 19th, which I'm very excited about!





### Misc

_Earlier project ideas - not currently planning to go forward with these
* How language changes over time
* How words have changed meaning over time
* Evolution of slang
* Character sentiment analysis: choose some subset of famous literary characters and analyze their dialogue
  to do sentiment analysis... challenge here would be to isolate a given character's dialogue, so not sure
  this is actually feasible._
