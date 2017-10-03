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
        self.lda_fp = self.rw_dir + self.distinguishing_str + '.model'
        self.iteration = 0
        self.corp_chunk = "initial"

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

    def _yield_corp_subset(self, corp_chunk_size):
        '''
        Hack corpus generator to deliver chunks of corpus of specified size
        '''
        self.corp_chunk = []
        for _ in range(corp_chunk_size):
            self.corp_chunk.extend(self.corpus)
        self.iteration += 1
        print "corpus chunk", self.iteration

    def update_lda(self, corp_chunk_size):
        '''
        Updates partial LDA model with latest chunk of the corpus
        '''

        if cores == 1:
            self.lda = ldamodel.LdaModel.load(self.lda_fp)
        else:
            self.lda = LdaMulticore.load(self.lda_fp)

        self._yield_corp_subset(corp_chunk_size)
        self.lda.update(self.corp_chunk)

        self._save_lda()

    def initialize_lda(self, num_topics, cores):
        '''
        Initializes lda model with given number of topics using the loaded corpus and dictionary
        '''
        if cores == 1:
            print "running single core"
            self.lda = ldamodel.LdaModel(corpus=None, alpha='auto', id2word=self.dictionary, num_topics=num_topics, update_every=0, passes=1) #passes=20)
        else:
            w = cores-1
            print "running multi-core"
            self.lda = LdaMulticore(corpus=None, id2word=self.dictionary, num_topics=num_topics, passes=1, workers=w) #passes=20

        self._save_lda()

    def _save_lda(self):
        '''
        Saves fitted lda model out to disk
        '''
        self.lda.save(self.lda_fp)


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
    corp_chunk_size = int(raw_input("Enter number of documents to be fitted at a time ('corpus chunk size'): "))
    cores = int(raw_input("Enter number of cores on your machine: "))
        #future improvement: any way for this script to query the rambo/vagrant setup files to determine # of cores?
    header = '../' + 'outputs-git_ignored/' #if problems move '/' down
    rw_dir = header + distinguishing_str + '/'

    LDAmod = LDAMaker(rw_dir, distinguishing_str)
    LDAmod.load_stuff()
    LDAmod.initialize_lda(num_topics, cores)

    print "model fitting beginning - this may take a while"
    while LDAmod.corp_chunk != []:
        LDAmod.update_lda(corp_chunk_size)

    #LDAmod.save_lda()
    print "model fitted and saved!"
