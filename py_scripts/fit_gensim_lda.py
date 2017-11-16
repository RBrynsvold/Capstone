from __future__ import print_function
from builtins import input
import os, codecs
import gensim
from gensim import corpora
from gensim.models import ldamodel
from gensim.models import LdaMulticore
from utils_streamers import CorpStreamer, BOWCorpStreamer, DirFileMgr

import logging
import itertools

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

# def head(stream, n=10):
#     """Convenience fnc: return the first `n` elements of the stream, as plain list."""
#     return list(itertools.islice(stream, n))


class LDAMaker(object):
    '''
    Contains everything to fit an LDA model
    '''
    def __init__(self, fps):
        self.fps = fps

    def load_stuff(self):
        '''
        Load up the dictionary (vocabulary) from file and the corpus as an object streamed from the dictionary
        '''

        self.dictionary = corpora.Dictionary.load(self.fps.dictionary_fp)
        self.corpus = BOWCorpStreamer(self.dictionary, self.fps.corp_lst_fp)

    def fit_lda(self, num_topics, cores, passes):
        '''
        Fits lda model with given number of topics using the loaded corpus and dictionary
        '''
        if cores == 1:
            print("running single core")
            self.lda = ldamodel.LdaModel(corpus=self.corpus,alpha='auto', id2word=self.dictionary, num_topics=num_topics, update_every=0, chunksize=2000, passes=passes)
        else:
            w = cores-1
            print("running multi-core")
            self.lda = LdaMulticore(corpus=self.corpus, id2word=self.dictionary, num_topics=num_topics, chunksize=2000, passes=passes, workers=w) #passes=20

        print(type(self.lda))

    def save_lda(self):
        '''
        Saves fitted lda model out to disk
        '''
        self.lda.save(self.fps.model_fp)


if __name__=='__main__':

    source_str = str(input("Enter identifier string for the corpus and dictionary from which to build the model: "))
    dest_str = str(input("Enter the identifier string to use for saving the model files: "))
    print(dest_str)
    num_topics = int(input("Enter number of topics (integer) to use for model fitting: "))
    passes = int(input("Enter the number of passes for fitting the model: "))
    cores = int(input("Enter number of cores on your machine: "))
        #future improvement: any way for this script to query the rambo/vagrant setup files to determine # of cores?
        #alternately/additionally, would like this script to reference a specs file, so it is tunable without having manually enter each parameter each time
        #or run from the command line as a function with args to get instructions, vs. long series of user inputs

    fps = DirFileMgr(source_str)
    fps.create_all_modeling_fps(dest_str)

    LDAmod = LDAMaker(fps)
    LDAmod.load_stuff()

    print("Model fitting beginning - this will take several minutes to several hours")
    LDAmod.fit_lda(num_topics, cores, passes)
    #look into adding that logging thing so I can tell what's going on

    LDAmod.save_lda()
    print("Model fitted and saved!")

    #To support more docs: try rewriting to fit model to smaller # of docs, then updating model - over and over until full corpus is processed??
