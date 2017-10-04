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

from nltk.corpus import stopwords
nltk.download('stopwords')
#^should I include download of nltk stopwords in my vagrant configuration?
#separate python script?
#needs to be done the first time, but not every time (take est. 3-5s)


class IterFile(object):
    '''
    File i/o and iteration utility
    '''
    def __init__(self, fname, root, mode='r', full_fp=None):
        if full_fp == None:
            self.filepath = root + fname
        else:
            self.filepath = full_fp
        self.file = codecs.open(self.filepath, mode, encoding='utf_8')

    def __iter__(self):
        '''
        Yield file lines after checking for unicode error
        '''
        try:
            for line in self.file:
                yield line
        except UnicodeDecodeError:
            print "unicode error caught"

    def write(self, line):
        self.file.write(line)

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
        self.transf_book_as_lst = []
        self.tok_book_as_lst =[]
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
        return [tok.strip(punctuation).lower().strip(punctuation) for tok in line.strip('\n').split() if tok.isalpha()]

    def _remove_stop_words(self, line):
        '''
        Get the stopwords list from nltk and take them out of the line
        '''
        return [tok for tok in line if tok not in self.stop]

    def transform(self):
        '''
        Call other class methods to perform document transformations.
        Record numerical counts for transformation analysis
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

        print self.iter_book.filepath, "has been processed"

        self.iter_book.close()


def create_save_objs(source_dir, outputs_dir, distinguishing_str, stop_words='Y', min_freq=5):
    #Note sure this function is really useful... need to eliminate in rewrite
    '''
    Call all subfunctions.
    Create and save gensim objects needed for lda model (corpus, dictionary).
    '''

    fileid_lst = get_fileid_lst(source_dir)
    books_lst_filep = outputs_dir + distinguishing_str + '_lst.txt'

    print "starting iteration thru corpus on disk"
    print "************************************************"

    dictionary, books_lst_filep, counts_dict = process_books(fileid_lst, books_lst_filep, outputs_dir, min_freq=min_freq)

    print "transformations and dictionary building complete"
    print "************************************************"

    save_stuff(distinguishing_str=distinguishing_str, dictionary=dictionary, corpus=None, counts_dict=counts_dict, outputs_dir=outputs_dir)

    print "Dimensional reduction complete!"


def process_books(fileid_lst, books_lst_filep, outputs_dir, min_freq):
    #Should probably rewrite as class obj....
    '''
    Iterate thru all books and create a dictionary.
    Save each 'book-as-list' to a file, to use later to create the corpus.
    '''

    print "extracting metadata - this should take a couple of minutes"
    metadata = readmetadata()
    #should change to IterFile object... for class rewrite, this obj can then be shared by freq filtering utility
    f = codecs.open(books_lst_filep, 'w', encoding='utf_8')
    stop = set(stopwords.words('english'))
    onek_books_lst, dicts_count = [], 0

    #setup directory to contain the numerous tmp_dicts output:
    dicts_fp = outputs_dir + 'tmp_dicts' + '/'
    print dicts_fp
    os.makedirs(dicts_fp)

    tokenized_word_count_l, tokenized_unique_l = [], []
    transf_word_count_l, transf_unique_l = [], []

    for num, f_id in enumerate(fileid_lst):
        adj_num = num + 1

        # get metadata
        title = get_book_title(f_id, metadata)

        current_book = BookUtil(f_id, source_dir, stop)
        current_book.transform()

        tokenized_word_count_l.append(current_book.tokenized_word_count)
        tokenized_unique_l.append(current_book.tokenized_unique)
        transf_word_count_l.append(current_book.transf_word_count)
        transf_unique_l.append(current_book.transf_unique)

        current_book_lst = current_book.transf_book_as_lst
        tmp_book_lst = [val for val in current_book_lst]

        onek_books_lst.append(tmp_book_lst)

        if adj_num % 1000 == 0:
            create_save_dicts(onek_books_lst, dicts_fp, dicts_count, final_merge='n')
            onek_books_lst = []
            dicts_count += 1

        f.write(title + ',' + u",".join(tmp_book_lst) + '\n')
    f.close()

    dictionary = create_save_dicts(onek_books_lst, dicts_fp, dicts_count, final_merge="y")

    tokenized_avg_words = int(sum(tokenized_word_count_l) / float(len(tokenized_word_count_l)))
    tokenized_avg_unique = int(sum(tokenized_unique_l) / float(len(tokenized_unique_l)))
    transf_avg_words = int(sum(transf_word_count_l) / float(len(transf_word_count_l)))
    transf_avg_unique = int(sum(transf_unique_l) / float(len(transf_unique_l)))

    transf_total_vocab = len(dictionary)
    tokenized_total_vocab = transf_total_vocab + len(stop)
    #I realize this is kind of cheating, but it is definitionally true and saves a TON of comp time/resources

    counts_dict = dict({'tokenized' : dict({'avg_words' : tokenized_avg_words, 'avg_unique' : tokenized_avg_unique, 'total_vocab' : tokenized_total_vocab}),  'tok_and_sw' : dict({'avg_words' : transf_avg_words, 'avg_unique' : transf_avg_unique, 'total_vocab' : transf_total_vocab})})

    if min_freq != None:
        dictionary, ff_word_count, ff_unique_count = frequency_filtering(dictionary, books_lst_filep, no_below=min_freq, no_above=0.40)

        ff_total_vocab = len(dictionary)

        counts_dict['freq_filtered'] = dict({'avg_words' : ff_word_count, 'avg_unique' : ff_unique_count, 'total_vocab' : ff_total_vocab})

    print "Results of dimensional reduction:",
    print "Tokenized:", counts_dict['tokenized']
    print "Stopword removal:", counts_dict['tok_and_sw']
    print "Frequency filtered", counts_dict['freq_filtered']

    return dictionary, books_lst_filep, counts_dict

def get_book_title(f_id, metadata):
    '''
    Query metadata based on file id
    '''
    #book_num = int(f_id.rstrip('.txt'))
    book_num = f_id.rstrip('.txt')

    try:
        title = metadata[book_num]['title']#.decode('utf-8')
    except KeyError:
        title = "NotAvailable"

    print title
    return title

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
        print "dictionary", n, "loaded & merged"

    print "merged all the dictionaries"


def create_save_dicts(tmp_books_lst, dicts_fp, dicts_count, final_merge="y"):
    '''
    Save out intermediate dictionaries.
    When all the files have been processed, save the last piece and merge all the dictionaries.
    '''
    d_tmp = corpora.dictionary.Dictionary()
    d_tmp.add_documents(tmp_books_lst)
    d_tmp.save(dicts_fp + str(dicts_count) + '.dict')

    print "added", len(d_tmp), "to temp dictionary", dicts_count

    if final_merge == 'y':
        final_dict = d_tmp #corpora.dictionary.Dictionary()
        for n in range(dicts_count):
            loaded_dict = corpora.dictionary.Dictionary.load(dicts_fp + str(n) + '.dict')
            final_dict.merge_with(loaded_dict)
            print "dictionary", n, "loaded & merged"
        return final_dict


def save_stuff(distinguishing_str, dictionary, corpus, counts_dict, outputs_dir):
    '''
    Create directory and save the outputs of the desired object(s)
    '''
    file_path = outputs_dir + distinguishing_str

    if dictionary != None:
        dictionary.save(file_path + '.dict')
    else:
        print "no dictionary to save"

    if corpus != None:
        corpora.MmCorpus.serialize(file_path + '_corpus.mm', corpus)
    else:
        print "No corpus to save"

    if counts_dict != None:
        json.dump(counts_dict, open(file_path + '_json.txt','w'))
    else:
        print "No counts to save"



##THIS GOES TOO SLOW -
#to add the freq filtering functionality back in (if time permits), need to do it like here: https://stackoverflow.com/questions/24688116/how-to-filter-out-words-with-low-tf-idf-in-a-corpus-with-gensim
def frequency_filtering(dictionary, books_lst_filep, no_below=5, no_above=0.40):
    '''
    Remove words that appear in less than 5 documents or more than 40 percent of documents
    '''
    #This should probably be another class method of books utils
    pass

    dictionary.filter_extremes(no_below=no_below, no_above=no_above)
    print "frequency filtering: starting dictionary set"
    s = set(dictionary.values())
    print "frequency filtering: finished dictionary set"

    #pull in the prev created corpus list file
    transf_corp_f = IterFile(fname=None, root=None, mode='r', full_fp=books_lst_filep)

    #create new corpus list file with frequency filtering (take out everything not in dict)
    tmp_fp = books_lst_filep + '.tmp'
    freq_filt_corp_f = IterFile(fname=None, root=None, mode='w', full_fp= tmp_fp)

    ff_word_count_lst, ff_unique_count_lst = [], []
    for num, book_line in enumerate(transf_corp_f):
        stripped_line = book_line.strip('/n').split(",")
        title = stripped_line[0]
        print title
        filtered_line = [tok for tok in stripped_line[1:] if tok in s]

        ff_word_count_lst.append(len(filtered_line))
        ff_unique_count_lst.append(len(set(filtered_line)))

        freq_filt_corp_f.write(title + ',' + u",".join(filtered_line) + '\n')
        print "book", num, "frequency-filtered"

    #make counts
    ff_word_count = int(sum(ff_word_count_lst) / float(len(ff_word_count_lst)))
    ff_unique_count = int(sum(ff_unique_count_lst) / float(len(ff_unique_count_lst)))

    #replace first corp list file with the one we just built
    os.rename(tmp_fp, books_lst_filep)

    return dictionary, ff_word_count, ff_unique_count


def get_fileid_lst(source_dir):
    '''
    Use NLTK to pull in the list of file ids in the given source directory
    '''
    temp_corp = PlaintextCorpusReader(source_dir, '.*\.txt')
    fileid_lst = temp_corp.fileids()

    return fileid_lst


if __name__=='__main__':
    #prompt user for needed info
    distinguishing_str = str(raw_input("Enter brief identifier string, to be appended to all outputs of this dimensional reduction: "))
    use_full_data = raw_input("Will you be using the full data set (y/n)?: ")
    #^ this is super useful for development but should be removed for final reproducibility code

    #create outputs directory which will be on the gitignore
        #reason: file sizes too large to be pushed to github - causes git problems if not excluded
    rel = '../'
    git_ignored_dir = rel + 'outputs-git_ignored'
    if not os.path.exists(git_ignored_dir):
        os.makedirs(git_ignored_dir)
    #create a directory for all outputs and subsequent reads for this run
        #reason: easy review of outputs... general sanity
    run_specific_file_path = git_ignored_dir + '/' + distinguishing_str
    if not os.path.exists(run_specific_file_path):
        os.makedirs(run_specific_file_path)
    else:
        print "saw output dir already existing and ignored"
    outputs_dir = run_specific_file_path + '/' #outputs_dir same both ways

    #relative filepaths - various options for various corp sizes for dev
    if use_full_data == 'n':
        which_partial = int(raw_input("What is the subset size? " ))
        if which_partial == 5000:
            source_dir = '../../5000_books' + '/'
        elif which_partial == 10000:
            source_dir = '../../10k_books' + '/'
        elif which_partial == 2500:
            source_dir = '../../2500_books' + '/'
        elif which_partial == 1000:
            source_dir = '../../1000_books' + '/'
        elif which_partial == 95:
            source_dir  = '../books/clean' + '/' #for 95-book practice data
        else:
            print "That subset is not available here"

        print "end of source_dir assignment script, source_dir = ", source_dir
    elif use_full_data == 'y':
        source_dir = '../../clean_books' + '/'  #for full data set
    elif use_full_data == 'merge':
        source_dir = 'skipping the source, yo!'
        dict_count = raw_input("How many dictionaries to merge?: ")
        merge_dicts(int(dict_count), outputs_dir)
    else:
        source_dir = 'invalid file path to raise error'
        print "please rerun and enter either 'y' or 'n' "

    print "Data source to be used: ", source_dir
    print "************************************************"

    #at end add print statement to remind user of string they entered (for lda call)

    if use_full_data != 'merge':
        create_save_objs(source_dir, outputs_dir, distinguishing_str, min_freq=5)
