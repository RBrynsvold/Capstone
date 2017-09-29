import os, codecs
import gensim
from gensim import corpora
from gensim.models import ldamodel
from gensim.models import LdaMulticore


def load_stuff(rw_dir, distinguishing_str):
    '''
    Load up the dictionary (vocabulary) and corpus
    '''
    dictionary = corpora.Dictionary.load(rw_dir + distinguishing_str + '.dict')
    corpus = corpora.MmCorpus(rw_dir + distinguishing_str + '_corpus.mm')

    return dictionary, corpus


def fit_lda(corpus, dictionary, num_topics):
    '''
    Fits lda model with given number of topics using the loaded corpus and dictionary
    '''
    lda = ldamodel.LdaModel(corpus=corpus,alpha='auto', id2word=dictionary, num_topics=num_topics, update_every=0, passes=20)

    return lda


def fit_multi_lda(corpus, dictionary, num_topics, cores):
    '''
    Same functionality as fit_lda, but reduces calc time with parallelization
    '''
    lda_multi = LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=20, workers=cores-1)

    return lda_multi


def save_model(model, rw_dir, distinguishing_str):
    '''
    Saves the model to the same directory that contains the corpus and dictionary files.  File extension .model extension
    '''
    model.save(rw_dir + distinguishing_str + '.model')


if __name__=='__main__':
#HARD-CODED relative filepaths
        #should rewrite with a 'specify' function that prompts user?
    rw_dir = '../outputs' + '/' # same both ways
    cores = 1

    distinguishing_str = str(raw_input("Enter identifier string for the corpus and dictionary from which to build the model: "))
    num_topics = int(raw_input("Enter number of topics (integer) to use for model fitting: "))
    #any way for this script to query the rambo/vagrant setup files to determine # of cores?

    dictionary, corpus = load_stuff(rw_dir, distinguishing_str)
    print "dictionary and corpus loaded"

    print "model fitting beginning - this may take a while"
    if cores == 1:
        model = fit_lda(corpus, dictionary, num_topics)
    else:
        model = fit_multi_lda(corpus, dictionary, num_topics, cores)

    save_model(model, rw_dir, distinguishing_str)
    print "model fitted and saved!"
