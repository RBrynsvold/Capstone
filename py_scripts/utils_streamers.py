from __future__ import print_function
from builtins import input
import os, codecs
from shutil import copy2

#File naming (for save or load) utility
class DirFileMgr(object):
    '''
    General-purpose utility to do directory and filepath management for the various inputs/outputs of the topic modeling
    project.  Intended to make file mgmt as automated and encapsulated as possible.

    :param {str} id_str:
        The unique identifier string for the run
    '''

    def __init__(self, id_str):
        self.id_str = id_str
        self.git_ignored_dir = '../../' + 'outputs-git_ignored'
        self.working_dir = self.git_ignored_dir + '/' + self.id_str

    def _check_make_dir(self, fp, brk='N'):
        '''
        GP check and make directory function
        Check to see if the directory you want to make already exists
        If it doesn't exist, make it
        If it does exist:
            Current behavior: break
            Future improvement: ask if you want to do it anyway, and/or give user chance to give different string
        '''
        if not os.path.exists(fp):
            os.makedirs(fp)
        else:
            if brk != 'N':
                print("WARNING: path already exists.")  
                print("Exit script now to avoid overwriting previous run.")
                #print("Rerun script and provide unused identifier string")
                #return "Exit program"

    def _setup_dirs(self, tmp_d='N'):
        '''
        Sets up directories in the architecture used for this project

        :param {str} tmp_d:
            Flag for temporary dictionaries directory - not always needed, so this toggles it on and off
        '''
        #if the directory does not already have an 'outputs-git_ignored' dir, then make it
            #reason for this dir: output file sizes too large to be pushed to github - causes git problems if not excluded
        self._check_make_dir(self.git_ignored_dir)

        self._check_make_dir(self.working_dir, brk='Y')

        if tmp_d != 'N':
            self.tmp_dict_dir = self.working_dir + '/tmp_dicts/'
            self._check_make_dir(self.tmp_dict_dir)

    def add_fp(self, obj):
        '''
        Add filepath to the DirFileMgr instance attributes.  Stores all the file naming conventions in one place
        #TODO: change all this to a dictionary??
        '''
        head = self.working_dir + '/' + self.id_str

        if obj == 'dictionary':
            self.dictionary_fp = head + '.dict'
            print("dictionary fp is assigned as ", self.dictionary_fp)
        elif obj == 'gensim_corpus':
            self.gensim_corp_fp = head + '_corpus.mm'
            print("corpus fp is assigned as ", self.gensim_corp_fp)
        elif obj == 'corp_lst':
            self.corp_lst_fp = head + '_lst.txt'
            print("corpus lst fp is assigned as ", self.corp_lst_fp)
        elif obj == 'counts_dict':
            self.counts_fp = head + '_json.txt'
            print("counts dictionary fp is assigned as ", self.counts_fp)
        elif obj == 'dr_run_params':
            self.dr_run_params = head + '_dr_run_params.txt'
            if not os.path.exists(self.dr_run_params):
                self._copy_rename_run_params(head, self.dr_run_params)
            print("dimensional reduction run parameters fp is assigned as ", self.dr_run_params)
        elif obj == 'model':
            self.model_fp = self.model_dir + '/' + self.model_str + '.model'
            print("model fp is assigned as ", self.model_fp)
        elif obj == 'mod_run_params':
            self.dr_run_params = head + '_dr_run_params.txt'
            self.mod_run_params = self.model_dir + '/' + self.model_str + '_mod_run_params.txt'
            if not os.path.exists(self.mod_run_params):
                self._copy_rename_run_params(self.model_dir, self.mod_run_params)
            print("modeling run parameters fp is assigned as ", self.mod_run_params)
        elif obj == 'pyLDAvis':
            self.pyldavis_fp = self.model_dir + '/' + self.model_str + '_ldavis.html'
            print("pyLDAvis html fp is assigned as ", self.pyldavis_fp)
        elif obj == 'source_dir':
            which_data = str(input("Which data set will be used? Enter either '5000' or 'full': "))
            #^ this is super useful for development but should be removed for final reproducibility code
            #relative filepaths - various options for various corp sizes for dev
            if which_data == '5000':
                self.source_dir = '../../5000_books' + '/'
            #     elif which_partial == 10000:
            #         source_dir = '../../10k_books' + '/'
            #     elif which_partial == 2500:
            #         source_dir = '../../2500_books' + '/'
            #     elif which_partial == 1000:
            #         source_dir = '../../1000_books' + '/'
                print("source dir is assigned as", self.source_dir)
            elif which_data == '95':
                self.source_dir  = '../books/clean' + '/' #for 95-book practice data
                print("source dir is assigned as", self.source_dir)
            elif which_data == 'full':
                self.source_dir = '../../full_corp_28k/clean_books' + '/'
            elif which_data == 'gpu-full':
                self.source_dir = '/data/ProjectGutenberg' + '/'
            else:
                print("Invalid entry for data source")
                #source_dir = '../../5000_books' + '/'

                print("Data source to be used: ", self.source_dir)
                print("************************************************")
        elif obj == 'coherence_model':
            self.coherence_model_fp = self.model_dir + '/' + self.model_str + '_coherence_model.'
            print("coherence model fp is assigned as ", self.coherence_model_fp)
        elif obj == 'coherence_df':
            self.coherence_df_fp = self.model_dir + '/' + self.model_str + '_coherence_df.csv'
            
        else:
            print("Type not recognized.  No filepath stored.")
            
    def _copy_rename_run_params(self, dest_dir, run_params_fp):
        '''
        Copies appropriate default run params file, saves it to relevant run directory, and renames it.

        :params {str} run_params_fp:
            Filepath to the json file containing the run parameters for the run
        '''
        if run_params_fp == self.dr_run_params:
            src_file = 'default_dr_run_params.txt'
        elif run_params_fp == self.mod_run_params:
            src_file = 'default_mod_run_params.txt'
        
        copy2('../'+src_file, run_params_fp)

    def create_all_dr_fps(self, new_setup='Y'):
        '''
        Automates creation of all the filepaths for a dimensional reduction run.

        :param {str} new_setup:
            Flag to toggle the new setup behavior on/off
        '''
        if new_setup == 'Y':
            self._setup_dirs(tmp_d='Y')
            self.add_fp('source_dir')
        self.add_fp('corp_lst')
        self.add_fp('dictionary')
        self.add_fp('counts_dict')
        self.add_fp('dr_run_params')
        #figure out a way to set up default run params

    def create_all_modeling_fps(self, model_str):
        '''
        Automates creation of all the filepaths for a dimensional reduction run.

        :param {str} model_str:
            Unique identifier string for the modeling run

        '''
        self.model_str = model_str
        self.model_dir = self.git_ignored_dir + '/' + self.model_str
        self._check_make_dir(self.model_dir)

        self.add_fp('corp_lst')
        self.add_fp('dictionary')
        self.add_fp('counts_dict')
        self.add_fp('model')
        self.add_fp('mod_run_params')

#GP file iteration utility
#needs work to make general - use a 'with codecs.open?'
#use inside of Corp Streamer?
class IterFile(object):
    '''
    File i/o and iteration utility

    :param {str} filepath:
        Filepath to the file being iterated
    :param {str} mode:
        Controls the file access mode.  Defaults to 'r' (read).
    :param {str} encoding:
        Encoding type for decoding the text file.  Defaults to 'utf_8'.

    '''
    def __init__(self, filepath, mode='r'):
        self.filepath = filepath
        self.file = codecs.open(self.filepath, mode, encoding='utf_8')

    def __iter__(self):
        '''
        Yield file lines (after checking for unicode error, if doing unicode check)
        '''
        try:
            for line in self.file:
                yield line
        except UnicodeDecodeError:
            print("unicode error caught")

    def write(self, line):
        """
        Writes a line to the file

        :param {str} line:
            Text line to be written
        """
        self.file.write(line)

    def close(self):
        '''
        Close file when done
        '''
        self.file.close()

#Corpus Streaming utility - as either tokens or vector
    #By 'corpus streaming' - I mean a generator to access the tokenized/processed text of the books from where it resides on disk


class CorpStreamer(object):
    """
    Streams a text-format corpus from location on disk

    :param {gensim.corpora.dictionary.Dictionary} dictionary:
        A gensim object containing the word-integer id mappings for the corpus
    :param {str} corp_lst_fp:
        Relative filepath to the corpus list
    :param {str} inc_title
        On/off switch for including the title in the streamed file (book) text
    """

    def __init__(self, dictionary, corp_lst_fp, inc_title='N'):
        self.dictionary = dictionary
        self.corp_lst_fp = corp_lst_fp
        self.inc_title = inc_title

    def __iter__(self):
        with codecs.open(self.corp_lst_fp, 'r', encoding='utf_8') as f:
            for line in f:
                if self.inc_title == 'N':
                    yield line.strip('/n').split(",")[1:]
                else:
                    yield line.strip('/n').split(",")

class BOWCorpStreamer(CorpStreamer):
    """
    Streams a bag-of-words-format corpus from location on disk

    :param {gensim.corpora.dictionary.Dictionary} dictionary:
        A gensim object containing the word-integer id mappings for the corpus
    :param {str} corp_lst_fp:
        Relative filepath to the corpus list
    :param {str} inc_title
        On/off switch for including the title in the streamed file (book) text
    """

    def __init__(self, dictionary, corp_lst_fp, inc_title='N'):
        self.dictionary = dictionary
        self.corp_lst_fp = corp_lst_fp
        self.inc_title = inc_title
        self.corp_stream = CorpStreamer(self.dictionary, self.corp_lst_fp, inc_title=self.inc_title)
        self.length = None

    def __iter__(self):
        for line in self.corp_stream:
            yield self.dictionary.doc2bow(line)

    def __len__(self):
        if self.length is None:
            # cache the corpus length
            self.length = sum(1 for line in self.corp_stream)
        return self.length
    
