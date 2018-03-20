from __future__ import print_function
from builtins import input
import os, codecs
import gensim
from gensim import corpora
from gensim.models import ldamodel
from gensim.models import LdaMulticore
import json
from utils_streamers import CorpStreamer, BOWCorpStreamer, DirFileMgr

import logging
import resource

import itertools

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

# def head(stream, n=10):
#     """Convenience fnc: return the first `n` elements of the stream, as plain list."""
#     return list(itertools.islice(stream, n))


class LDAMaker(object):
    '''
    Collection of information, objects, and methods to fit an LDA model

    :param {DirFileMgr obj} fps:
        Class object that contains all the filepaths for the current task as object attributes
    :param {dict(str, int/str)} run_params:
        Dictionary containing all the parameters for the present run
    '''
    def __init__(self, fps, run_params):
        self.fps = fps
        self.run_params = run_params

    def load_stuff(self):
        '''
        Load up the dictionary (vocabulary) from file and the corpus as an object streamed from the dictionary
        '''

        self.dictionary = corpora.Dictionary.load(self.fps.dictionary_fp)
        self.corpus = BOWCorpStreamer(self.dictionary, self.fps.corp_lst_fp)

    def fit_lda(self):
        '''
        Fits lda model with given number of topics using the loaded corpus and dictionary
        '''
        if self.run_params['cores'] == 1:
            print("running single core")
            self.lda = ldamodel.LdaModel(corpus=self.corpus, alpha='auto', id2word=self.dictionary, **self.run_params)

                # corpus=self.corpus,alpha='auto', id2word=self.dictionary, \
                # num_topics=self.run_params['num_topics'], update_every=self.run_params['update_every'], \
                # chunksize=self.run_params['chunksize'], passes=self.run_params['passes'])
        else:
            print("running multi-core")
            self.lda = LdaMulticore(corpus=self.corpus, id2word=self.dictionary, num_topics=self.run_params['num_topics'], chunksize=self.run_params['chunksize'], passes=self.run_params['passes'], workers=self.run_params['cores']-1)

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

    fps = DirFileMgr(source_str)
    fps.create_all_modeling_fps(dest_str)

    with open(fps.mod_run_params) as run_params_f:
        #add 'try' statement logic
        run_params = json.load(run_params_f)
        run_params['dim_reduction_run_used'] = source_str
    json.dump(run_params, open(fps.mod_run_params, 'w'))
    print ("The selected run parameters are:")
    print (run_params)

    LDAmod = LDAMaker(fps, run_params)
    LDAmod.load_stuff()

    #future improvement: any way for this script to query the rambo/vagrant setup files to determine # of cores?

    print("Model fitting beginning - this will take several minutes to several hours")
    LDAmod.fit_lda()
    
    LDAmod.save_lda()
    print("Model fitted and saved!")

    #To support more docs: try rewriting to fit model to smaller # of docs, then updating model - over and over until full corpus is processed??

# print 'Memory usage: %s (kb)' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss