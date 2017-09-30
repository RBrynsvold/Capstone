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

from nltk.corpus import stopwords
#nltk.download('stopwords')
#^should I include download of nltk stopwords in my vagrant configuration?


class IterFile(object):
    '''
    File i/o and iteration utility
    '''
    def __init__(self, fname, root):
        self.filepath = root + fname
        self.file = codecs.open(self.filepath, 'r', encoding='utf_8')

    def __iter__(self):
        '''
        Yield file lines after checking for unicode error
        '''
        try:
            for line in self.file:
                yield line
        except UnicodeDecodeError:
            print "unicode error caught"

    def close(self):
        '''
        Close file when done
        '''
        self.file.close()


class BookUtil(object):
    '''
    Performs the transformations on a book and stores the associated information
    '''

    def __init__(self, fname, root, stop):
        self.iter_book = IterFile(fname, root)
        self.dictionary = corpora.dictionary.Dictionary()
        self.book_as_lst = []
        self.stop = stop

    def _empty_line_check(self, line) :
        '''
        checks for empty line
        '''
        if line == "\n":
            empty = True
        else:
            empty = False
        return empty

    def _basic_tokenize(self,line):
        '''
        convert to list
        strip punctuation, lowercase
        '''
        return [tok.lower().strip(punctuation) for tok in line.strip('\n').split()]

    def _remove_stop_words(self, line):
        '''
        Get the stopwords list from nltk and take them out of the line
        '''
        return [tok for tok in line if tok not in self.stop]

    def transform(self):
        '''
        Call other class methods to
        '''
        for line in self.iter_book:
            if self._empty_line_check(line) == False:
                line = self._basic_tokenize(line)
                line = self._remove_stop_words(line)
                self.book_as_lst.append(line)
        #self.dictionary.add_documents(self.book_as_lst)

        print self.iter_book.filepath, "has been processed"

        self.iter_book.close()


def create_save_objs(source_dir, outputs_dir, distinguishing_str, stop_words='Y', min_freq=1):
    '''
    Call all subfunctions.
    Create and save gensim objects needed for lda model (corpus, dictionary).
    '''
    fileid_lst = get_fileid_lst(source_dir)
    books_lst_filep = '../' + distinguishing_str + '_lst.txt'

    print "starting iteration thru corpus"
    print "************************************************"

    dictionary, books_lst_filep = process_books(fileid_lst, books_lst_filep, outputs_dir)

    print "transformations and dictionary building complete"
    print "************************************************"

    corpus = create_corp(dictionary, books_lst_filep, outputs_dir)

    print "corpus complete"
    print "************************************************"

    # avg_num_tokens, avg_unique_toks, dictionary_length, toks_per_fileid, unique_toks_per_fileid = dim_red_counts(fileid_lst, all_transf_books_lst, dictionary, corpus)

    save_stuff(distinguishing_str=distinguishing_str, dictionary=dictionary, corpus=corpus, outputs_dir=outputs_dir)

    print "Dimensional reduction complete!"
    print "After dimensional reduction:"
    print "   "
    # print "Average total tokens per book:        ", avg_num_tokens
    # print "Average unique tokens per book:       ", avg_unique_toks
    # print "Number of unique words in vocabulary: ", dictionary_length

    # return avg_num_tokens, avg_unique_toks, dictionary_length, toks_per_fileid, unique_toks_per_fileid
    #need to write dimensionality reduction stuff to file for review

def process_books(fileid_lst, books_lst_filep, outputs_dir):
    '''
    Iterate thru all books and create a dictionary.
    Save each 'book-as-list' to a file, to use later to create the corpus.
    '''
    f = codecs.open(books_lst_filep, 'w', encoding='utf_8')
    stop = set(stopwords.words('english'))
    onek_books_lst, dicts_count = [], 0
    dicts_fp = outputs_dir + 'tmp_dicts/'

    for num, f_id in enumerate(fileid_lst):
        adj_num = num + 1

        current_book = BookUtil(f_id, source_dir, stop)
        current_book.transform()

        current_book_lst = current_book.book_as_lst
        tmp_book_lst = [val for sublist in current_book_lst for val in sublist]

        onek_books_lst.append(tmp_book_lst)

        if adj_num % 1000 == 0:
            create_save_dicts(onek_books_lst, dicts_fp, dicts_count, final_merge='n')
            onek_books_lst = []
            dicts_count += 1

        f.write(u",".join(tmp_book_lst) + '\n')

    dictionary = create_save_dicts(onek_books_lst, dicts_fp, dicts_count, final_merge="y")

    print "returned dictionary is this size: ", len(dictionary)

    f.close()

    print "returning the books list file path " + books_lst_filep

    return dictionary, books_lst_filep


def create_save_dicts(tmp_books_lst, dicts_fp, dicts_count, final_merge="y"):
    '''
    Save out intermediate dictionaries.
    When all the files have been processed, save the last piece and merge all the dictionaries.
    '''
    d_tmp = corpora.dictionary.Dictionary()
    d_tmp.add_documents(tmp_books_lst)
    d_tmp.save(dicts_fp + str(dicts_count) + '.dict')

    print "added ", len(d_tmp), " to temp dictionary"

    if final_merge == 'y':
        final_dict = d_tmp #corpora.dictionary.Dictionary()
        for n in range(dicts_count):
            loaded_dict = corpora.dictionary.Dictionary.load(dicts_fp + str(n) + '.dict')
            final_dict.merge_with(loaded_dict)
            print "dictionary", n, "loaded & merged"
        return final_dict

def create_corp(dictionary, books_lst_filep, source_dir):
    '''
    Open big file of 'books-as-lists', stream it in, and use to create corpus.
    '''
    f = IterFile(books_lst_filep, '')

    #print "the file ", f.file.name

    corpus = [dictionary.doc2bow(book.strip('/n').split(',')) for book in f]

    return corpus

def dim_red_counts(fileid_lst, all_transf_books_lst, dictionary, corpus):
    '''
    Create all the counts used to show progress of dimensional reduction
    '''
    #note this only shows final - would need to adapt to show stepwise reduction
    #will probably stick with the jupyter for that for now

    #for viewing convenience (and used below)
    toks_per_fileid = [(tup[0], len(tup[1])) for tup in zip(fileid_lst, all_transf_books_lst)]
    #could actually do this better by redoing like it was done for the unique_toks stuff

    avg_num_tokens = int(np.mean([pair[1] for pair in toks_per_fileid]))
    #changed this from what I had in jn to avoid going thru full text again
    #avg_num_tokens = int(np.mean([len(book) for book in all_transf_books_lst]))

    unique_toks_num_lst = [len(book) for book in corpus]
    avg_unique_toks = int(np.mean(unique_toks_num_lst))
    unique_toks_per_fileid = zip(fileid_lst, unique_toks_num_lst)

    dictionary_length = len(dictionary)

    return avg_num_tokens, avg_unique_toks, dictionary_length, toks_per_fileid, unique_toks_per_fileid


def save_stuff(distinguishing_str, dictionary, corpus, outputs_dir):
    '''
    Create directory and save the outputs of the desired object(s)
    '''
##this does not work - no dir is being made - troubleshoot
    file_path = outputs_dir + distinguishing_str
    # directory = os.path.dirname(file_path)
    # if not os.path.exists(directory):
    #     os.makedirs(directory)

    if dictionary != None:
        dictionary.save(file_path + '.dict')
    else:
        print "no dictionary to save"

    if corpus != None:
        corpora.MmCorpus.serialize(file_path + '_corpus.mm', corpus)
    else:
        print "No corpus to save"


##THIS GOES TOO SLOW -
#to add the freq filtering functionality back in (if time permits), need to do it like here: https://stackoverflow.com/questions/24688116/how-to-filter-out-words-with-low-tf-idf-in-a-corpus-with-gensim
def frequency_filtering(book_as_lst, n):
    '''
    Remove words that appear less than n times
    '''
    all_tokens_set = set(book_as_lst)
    tokens_once = set(word for word in all_tokens_set if book_as_lst.count(word) <= n)

    return [word for word in book_as_lst if word not in tokens_once]


def get_fileid_lst(source_dir):
    '''
    Use NLTK to pull in the list of file ids in the given source directory
    '''
    temp_corp = PlaintextCorpusReader(source_dir, '.*\.txt')
    fileid_lst = temp_corp.fileids()

    return fileid_lst


if __name__=='__main__':

    use_full_data = raw_input("Will you be using the full data set (y/n)?: ")
    distinguishing_str = str(raw_input("Enter brief identifier string, to be appended to all outputs of this dimensional reduction: "))

    #relative filepaths
    if use_full_data == 'n':
        source_dir  = '../books/clean' + '/' #for 95-book practice data
    elif use_full_data == 'y':
        source_dir = '../../clean_books' + '/'  #for full data set
    else:
        source_dir = 'invalid file path to raise error'
        print "please rerun and enter either 'y' or 'n' "

    print "Data source to be used: ", source_dir
    print "************************************************"

    outputs_dir = '../outputs' + '/' # same both ways

    create_save_objs(source_dir, outputs_dir, distinguishing_str)

    ##Backup: hardcoded dir options
    #source_dir = '/home/ubuntu/data_download/clean_books/'
    #outputs_dir = '/home/ubuntu/Capstone/outputs/full_data/'
    #source_dir = '/Users/rachelbrynsvold/dsi/capstone_dir/Capstone/books/clean' + '/'
    #outputs_dir = '/Users/rachelbrynsvold/dsi/capstone_dir/Capstone/outputs/junk' + '/'
