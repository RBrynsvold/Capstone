
# Project 1: Literary Analysis with NLP in collaboration with Terminal Labs

__Goal__: Gain some insight about literary texts using NLP.  I haven't settled yet on the exact analysis I wantto do, but some ideas I've had floating around are:
* Predicting authorship of books, based on other works by that other (training set = one set of his/her
  books, test set = another set)
* Grouping books by thematic elements via latent feature analysis (SVD/PCA/as appropriate)
* Character sentiment analysis: choose some subset of famous literary characters and analyze their dialogue
  to do sentiment analysis... challenge here would be to isolate a given character's dialogue, so not sure
  this is actually feasible.
There's really so much possibility here - the issue is going to be narrowing it down!

Data Source: [Project Gutenberg ] (http://www.gutenberg.org/wiki/Gutenberg:Information_About_Robot_Access_to_our_Pages) has full text of 54,000 (!!) public domain books available for download!  This would be a really great dataset to use to play with NLP.  I am pretty confident I'll be able to obtain and use this dataset, but it's a little involved to get started, and so I haven't validated this assumption yet.  So I guess this is my 'I think I can get the data' proposal.

__Presentation Format__: Slides

### Terminal Labs collaboration

My Terminal Labs contact (Michael Verhulst, CIO) and I have tentatively agreed to go ahead with a collaboration 
on my NLP project.  
Their interest in the project is use of and exposure for their open-source [project Rambo](https://github.com/terminal-labs/rambo).  From the project github:

>This repo is for provisioning and configuration of virtual machines (and containers) in a simple and predictable way. Just run one command and your vms is up, code is deployed and your app is running, on any supported platform.

>At this time the repo allows you to create a debian 8 Jessie VM on multiple providers (AWS EC2, Digitalocean, Virtualbox, lxc) The base machine configuration is a debian 8 Jessie 64bit os with 1024mb ram, and 30GB drive.

