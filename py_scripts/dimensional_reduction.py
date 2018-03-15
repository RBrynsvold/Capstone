from __future__ import print_function
from builtins import input
import os, codecs
import gensim
from gensim import corpora
from collections import defaultdict
import string
from string import punctuation
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
import pandas as pd
import numpy as np
import nltk
import json
import rdflib
from metadata_extraction import readmetadata
from utils_streamers import DirFileMgr, IterFile

from nltk.corpus import stopwords
nltk.download('stopwords')
#^should I include download of nltk stopwords in my vagrant configuration?
#separate python script?
#needs to be done the first time, but not every time (take est. 3-5s)

class BookUtil(object):
    '''
    Performs the transformations on a book and stores the associated information

    :param {str} f_id:
        The name of the individual data file
    :param {str} source_dir:
        The relative path to the source directory that contains all the data (book) files
    :param {set<str>} stop:
        Set of english stopwords (from NLTK)
    '''

    def __init__(self, f_id, source_dir, stop):
        self.iter_book = IterFile(source_dir + f_id)
        self.dictionary = corpora.dictionary.Dictionary()
        self.transf_book_as_lst = []
        self.tok_book_as_lst =[]
        self.stop = stop

    def _empty_line_check(self, line) :
        '''
        Checks for empty line

        :param {str} line:
            The line of text to be checked
        :return {bool} empty:
            A True/False response for whether the line is empty
        '''
        if line == "\n":
            empty = True
        else:
            empty = False
        return empty

    def _basic_tokenize(self,line):
        '''
        Splits a line (converts to a list of strings), then strips punctuation, makes lowercase.  Also eliminates
            tokens containing non-alphabet characters.

        :param {str} line:
            The line of text to be tokenized
        :return {list<str>}:
        '''
        return [tok.strip(punctuation).lower().strip(punctuation) for tok in line.strip('\n').split() if tok.isalpha()]

    def _remove_stop_words(self, line):
        '''
        Removes stopwords from the tokenized line

        :param {list<str>} line:
            Tokenized partially-processed line
        :return {list<str>}
            Further processed line
        '''
        return [tok for tok in line if tok not in self.stop]

    def transform(self):
        '''
        Calls other class methods to perform document transformations.  Records numerical counts for transformation
            analysis.
        '''
        self.tok_book_as_lst, self.transf_book_as_lst = [], []

        for num, line in enumerate(self.iter_book):
            if self._empty_line_check(line) == False:
                line = self._basic_tokenize(line)
                self.tok_book_as_lst.extend(line)
                line = self._remove_stop_words(line)
                self.transf_book_as_lst.extend(line)

        #calc and assign counts at end of book
        self.tokenized_word_count = len(self.tok_book_as_lst)
        self.tokenized_unique = len(set(self.tok_book_as_lst))
        self.transf_word_count = len(self.transf_book_as_lst)
        self.transf_unique = len(set(self.transf_book_as_lst))

        print(self.iter_book.filepath, "has been processed")

        self.iter_book.close()


def process_books(fps, min_freq, run_params):
    #Should probably rewrite as class obj? Maybe not?
    #Rewrote filepath mgmt as class obj - that might have done what I wanted
    '''
    Iterates through all text data files (books) and creates a dictionary.  Saves each 'book-as-list' to a file, to use
        later to create the BOW corpus.

    :param {DirFileMgr obj} fps:
        Class object that contains all the filepaths for the current task as object attributes
    TODO: min_freq is redundant with run_params['min_freq'] - update to fix
    :param {int} min_freq:
        The minimum number of documents that a token must appear in to be kept in the corpus dictionary
    :param {dict(str, int/str)} run_params:
        Dictionary containing all the parameters for the present run
    :return {gensim.corpora.dictionary.Dictionary} dictionary:
        A gensim object containing the word-integer id mappings for the entire corpus
    :return {dict(str, int)} counts_dict:

    '''
    fileid_lst = get_fileid_lst(fps.source_dir)

    print("Extracting metadata - this should take a couple of minutes")
    metadata = readmetadata()
    #should change to IterFile object... for class rewrite, this obj can then be shared by freq filtering utility
    f = codecs.open(fps.corp_lst_fp, 'w', encoding='utf_8')
    stop = set(stopwords.words('english'))
    onek_books_lst, dicts_count = [], 0

    tokenized_word_count_l, tokenized_unique_l = [], []
    transf_word_count_l, transf_unique_l = [], []

    for num, f_id in enumerate(fileid_lst):
        adj_num = num + 1

        # get metadata
        title = get_book_title(f_id, metadata)

        current_book = BookUtil(f_id, fps.source_dir, stop)
        current_book.transform()

        tokenized_word_count_l.append(current_book.tokenized_word_count)
        tokenized_unique_l.append(current_book.tokenized_unique)
        transf_word_count_l.append(current_book.transf_word_count)
        transf_unique_l.append(current_book.transf_unique)

        current_book_lst = current_book.transf_book_as_lst
        tmp_book_lst = [val for val in current_book_lst]

        onek_books_lst.append(tmp_book_lst)

        if adj_num % 1000 == 0:
            create_save_dicts(onek_books_lst, fps.tmp_dict_dir, dicts_count, final_merge='n')
            onek_books_lst = []
            dicts_count += 1

        f.write(title + ',' + u",".join(tmp_book_lst) + '\n')
    f.close()

    dictionary = create_save_dicts(onek_books_lst, fps.tmp_dict_dir, dicts_count, final_merge="y")

    tokenized_avg_words = int(sum(tokenized_word_count_l) / float(len(tokenized_word_count_l)))
    tokenized_avg_unique = int(sum(tokenized_unique_l) / float(len(tokenized_unique_l)))
    transf_avg_words = int(sum(transf_word_count_l) / float(len(transf_word_count_l)))
    transf_avg_unique = int(sum(transf_unique_l) / float(len(transf_unique_l)))

    transf_total_vocab = len(dictionary)
    tokenized_total_vocab = transf_total_vocab + len(stop)
    #I realize this is kind of cheating for the counts, but it is definitionally true and saves a TON of comp time/resources

    counts_dict = dict({'tokenized' : dict({'avg_words' : tokenized_avg_words, 'avg_unique' : tokenized_avg_unique, 'total_vocab' : tokenized_total_vocab}),  'tok_and_sw' : dict({'avg_words' : transf_avg_words, 'avg_unique' : transf_avg_unique, 'total_vocab' : transf_total_vocab})})

    #this logic needs to be updated - min_freq is a redundant variable
    if min_freq != None:
        dictionary, ff_word_count, ff_unique_count = frequency_filtering(dictionary, fps.corp_lst_fp, no_below=run_params['min_freq'], no_above=run_params['max_freq'], keep_n=run_params['keep_n'])

        ff_total_vocab = len(dictionary)

        counts_dict['freq_filtered'] = dict({'avg_words' : ff_word_count, 'avg_unique' : ff_unique_count, 'total_vocab' : ff_total_vocab})

    print("Results of dimensional reduction:", end=' ')
    print("Tokenized:", counts_dict['tokenized'])
    print("Stopword removal:", counts_dict['tok_and_sw'])
    print("Frequency filtered", counts_dict['freq_filtered'])

    return dictionary, counts_dict

def get_book_title(f_id, metadata):
    '''
    Query metadata based on file id

    :param {str} f_id:
        Name of the text data file (book) for which we need title
    :param {dict(str, <various types>)} metadata:
        Dictionary containing all the metadata available from Gutenberg website's XML file.  See metadata_extraction.py
        for source
    :return {str} title:
        The title of book contained in the text data file of interest.
    '''
    book_num = int(f_id.rstrip('.txt'))
    #book_num = f_id.rstrip('.txt')  # doesn't work b/c metadata index expects int

    try:
        title = metadata[book_num]['title']#.decode('utf-8')
    except KeyError:
        title = "NotAvailable"

    print(title)
    return title

#dont think I'm actually using this function anymore??
def merge_dicts(dicts_count, outputs_dir):
    '''
    Merge dictionaries together that have been created from a previous pass
    '''
    from gensim import corpora
    dicts_fp = outputs_dir + 'tmp_dicts'

    final_dict = corpora.dictionary.Dictionary()
    for n in range(dicts_count + 1):
        loaded_dict = corpora.dictionary.Dictionary.load('tmp_dict_' + str(n) + '.dict')
        final_dict.merge_with(loaded_dict)
        print("dictionary", n, "loaded & merged")

    print("merged all the dictionaries")


def create_save_dicts(tmp_books_lst, dicts_fp, dicts_count, final_merge="y"):
    '''
    Saves intermediate dictionaries to file in order to prevent RAM overload during run.

    When all the files have been processed, saves the last piece and merge all the dictionaries.

    :param {list(list(str))} tmp_books_lst:
        A list containing the processed text for each book in the current chunk, each as a list of tokens (strings)
    :param {str} dicts_fp:
        Filepath where dictionaries are to be saved.
    :param {int} dicts_count:
        Count of the present chunk of books ('chunk x of y')
    :param {str} final_merge:
        Flag for the final merge step.  If 'y', then go forward with the final merge.
    :return {gensim.corpora.dictionary.Dictionary} dictionary:
        If run in the final merge case, will return a combined gensim dictionary object for the whole corpus

    '''
    d_tmp = corpora.dictionary.Dictionary()
    d_tmp.add_documents(tmp_books_lst)
    d_tmp.save(dicts_fp + str(dicts_count) + '.dict')

    print("added", len(d_tmp), "to temp dictionary", dicts_count)

    if final_merge == 'y':
        final_dict = d_tmp #corpora.dictionary.Dictionary()
        for n in range(dicts_count):
            loaded_dict = corpora.dictionary.Dictionary.load(dicts_fp + str(n) + '.dict')
            final_dict.merge_with(loaded_dict)
            print("dictionary", n, "loaded & merged")
        return final_dict

def frequency_filtering(dictionary, corp_lst_filep, no_below=5, no_above=0.5, keep_n=2000000):
    '''
    Remove words that appear in less than no_below documents or more than no_above proportion of documents

    :param {gensim.corpora.dictionary.Dictionary} dictionary:
        A gensim object containing the word-integer id mappings for the entire corpus
    :param {str} corp_lst_filep:
        The relative path for the file containing the entire processed corpus in text form - one file/book per line
    :param {int} no_below:
        The minimum number of documents that a token must appear in to be kept in the corpus dictionary.  Defaults to 5.
    :param {int} no_above:
        The maximum proportion of the corpus that a token can appear in before being removed.  Defaults to 0.5
    :param {int} keep_n:
        Number of dictionary terms to keep.  Terms in excess of this number are discarded.
    :return {gensim.corpora.dictionary.Dictionary} dictionary:
        A gensim object containing the word-integer id mappings for the entire corpus - now frequncy filtered
    :return {int} ff_word_count:
        Total word count after frequency filtering
    :return {int} ff_unique_count
        Count of unique words after frequency filtering
    '''
    #This should probably be another class method of bookS utils?

    dictionary.filter_extremes(no_below=no_below, no_above=no_above, keep_n=keep_n)
    print("frequency filtering: starting dictionary set")
    s = set(dictionary.values())
    print("frequency filtering: finished dictionary set")

    #pull in the prev created corpus list file
    transf_corp_f = IterFile(corp_lst_filep, mode='r')

    #create new corpus list file with frequency filtering (take out everything not in dict)
    tmp_fp = corp_lst_filep + '.tmp'
    freq_filt_corp_f = IterFile(tmp_fp, mode='w')

    ff_word_count_lst, ff_unique_count_lst = [], []
    for num, book_line in enumerate(transf_corp_f):
        stripped_line = book_line.strip('/n').split(",")
        title = stripped_line[0]
        print(title)
        filtered_line = [tok for tok in stripped_line[1:] if tok in s]

        ff_word_count_lst.append(len(filtered_line))
        ff_unique_count_lst.append(len(set(filtered_line)))

        freq_filt_corp_f.write(title + ',' + u",".join(filtered_line) + '\n')
        print("book", num, "frequency-filtered")

    #make counts
    ff_word_count = int(sum(ff_word_count_lst) / float(len(ff_word_count_lst)))
    ff_unique_count = int(sum(ff_unique_count_lst) / float(len(ff_unique_count_lst)))

    #replace first corp list file with the one we just built
    os.rename(tmp_fp, corp_lst_filep)

    return dictionary, ff_word_count, ff_unique_count


def get_fileid_lst(source_dir):
    '''
    Use NLTK to pull in the list of file ids in the given source directory

    :param {str} source_dir:
        The relative path to the source directory that contains all the data (book) files
    :return {str} fileid_lst:
        List of all file id's ending in '.txt' in the source_dir
    '''
    temp_corp = PlaintextCorpusReader(source_dir, '.*\.txt')
    fileid_lst = temp_corp.fileids()

    return fileid_lst


if __name__=='__main__':
    #prompt user for needed info
    id_str = str(input("Enter brief identifier string, to be appended to all outputs of this dimensional reduction: "))

    fps = DirFileMgr(id_str)
    fps.create_all_dr_fps()

    with open(fps.dr_run_params) as run_params_f:
        #add 'try' statement logic
        run_params = json.load(run_params_f)
        run_params['dataset'] = fps.source_dir
    json.dump(run_params, open(fps.dr_run_params, 'w'))
        
    print (run_params)

    print("starting iteration thru corpus on disk")
    print("************************************************")

    dictionary, counts_dict = process_books(fps, min_freq=run_params['min_freq'], run_params=run_params)

    print("transformations and dictionary building complete")
    print("************************************************")

    dictionary.save(fps.dictionary_fp)
    json.dump(counts_dict, open(fps.counts_fp, 'w'))

    print("Dimensional reduction complete!")
    print("Use", id_str, "as the identifier string for the model fitting script.")
