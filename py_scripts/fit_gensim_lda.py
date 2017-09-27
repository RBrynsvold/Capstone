import os, codecs
import gensim
from gensim.models import ldamodel
from gensim.models import LdaMulticore

def load_stuff():

def fit_save_lda(corpus):
    lda = ldamodel.LdaModel(corpus=corpus,alpha='auto', id2word=dictionary, num_topics=100, update_every=0, passes=20)

def fit_save_multi_lda(corpus, dictionary, num_topics, cores):
    lda_multi = LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=20, workers=cores-1)

def save_stuff(model, type):
    model.save()

if __name__=='__main__':
    #should rewrite with a 'specify' function that prompts user?
    sources_dir = SOMETHING + '/'
    outputs_dir = SOMETHING + '/'
    cores =

    load_stuff()
    if cores = 1:
        fit_save_lda()
    else:
        fit_save_multi_lda()
