import os, codecs
import gensim
from gensim import corpora
from gensim.models import ldamodel
from gensim.models import LdaMulticore

import logging
import itertools

logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO)
logging.root.level = logging.INFO  # ipython sometimes messes up the logging setup; restore

def head(stream, n=10):
    """Convenience fnc: return the first `n` elements of the stream, as plain list."""
    return list(itertools.islice(stream, n))


class LDAMaker(object):
    '''
    Contains everything to fit an LDA model
    '''
    def __init__(self, rw_dir, distinguishing_str):
        self.rw_dir = rw_dir
        self.distinguishing_str = distinguishing_str

    def load_stuff(self):
        '''
        Load up the dictionary (vocabulary) from file and the corpus as an object streamed from the dictionary
        '''
        dict_fp = self.rw_dir + self.distinguishing_str + '.dict'
        corp_lst_fp = self.rw_dir + self.distinguishing_str + '_lst.txt'

        # dict_fp = self.rw_dir + self.distinguishing_str + '.dict'
        # corp_lst_fp = '../../' + self.distinguishing_str + '_lst.txt'

        self.dictionary = corpora.Dictionary.load(dict_fp)
        self.corpus = CorpStreamer(self.dictionary, corp_lst_fp)

    def fit_lda(self, num_topics, cores, passes):
        '''
        Fits lda model with given number of topics using the loaded corpus and dictionary
        '''
        if cores == 1:
            print "running single core"
            self.lda = ldamodel.LdaModel(corpus=self.corpus,alpha='auto', id2word=self.dictionary, num_topics=num_topics, update_every=0, chunksize=2000, passes=passes)
        else:
            w = cores-1
            print "running multi-core"
            self.lda = LdaMulticore(corpus=self.corpus, id2word=self.dictionary, num_topics=num_topics, chunksize=2000, passes=passes, workers=w) #passes=20

        print type(self.lda)

    def save_lda(self):
        '''
        Saves fitted lda model out to disk
        '''
        lda_fp = self.rw_dir + self.distinguishing_str + '.model'
        self.lda.save(lda_fp)


class CorpStreamer(object):
    '''
    Class to stream a corpus from a saved dictionary and a corpus in the form of a single saved list.
    Assumes pre-processed corpus list, with one book per line, all tokens separated by commas.
    '''
    def __init__(self, dictionary, corp_lst_fp):
        self.dictionary = dictionary
        self.corp_lst_fp = corp_lst_fp

    def __iter__(self):
        with codecs.open(self.corp_lst_fp, 'r', encoding='utf_8') as f:
            for line in f:
                yield self.dictionary.doc2bow(line.strip('/n').split(","))


if __name__=='__main__':

    distinguishing_str = str(raw_input("Enter identifier string for the corpus and dictionary from which to build the model: "))
    num_topics = int(raw_input("Enter number of topics (integer) to use for model fitting: "))
    passes = int(raw_input("Enter the number of passes for fitting the model: "))
    cores = int(raw_input("Enter number of cores on your machine: "))
        #future improvement: any way for this script to query the rambo/vagrant setup files to determine # of cores?
    #should change back to source_dir and outputs_dir, so I can save the new elsewhere (multiple models from same dim red)
    header = '../' + 'outputs-git_ignored/' #if problems move '/' down
    rw_dir = header + distinguishing_str + '/'

    LDAmod = LDAMaker(rw_dir, distinguishing_str)
    LDAmod.load_stuff()

    print "model fitting beginning - this may take a while"
    LDAmod.fit_lda(num_topics, cores, passes)
    #look into adding that logging thing so I can tell what's going on

    LDAmod.save_lda()
    print "model fitted and saved!"

    #probably should have script make a subdir for multiple models from the same dim reduction
