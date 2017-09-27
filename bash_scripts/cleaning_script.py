import sys, os, codecs

def clean():

    #path_head is HARD-CODED - change if new file structure!
    raw_path_head = "/home/ubuntu/data_download/final_txt_files/"
    clean_path_head = "/home/ubuntu/data_download/clean_books/"

    #get list of text file names to iterate thru
    fname = "/home/ubuntu/Capstone/filepaths.txt"
    with codecs.open(fname, 'r', encoding='utf_8') as f:
        content = f.readlines()
    txt_file_lst = [x.strip('\n') for x in content]
    ##
    for file_name in txt_file_lst:
        raw_path = raw_path_head + file_name
        clean_path = clean_path_head + file_name

        clean_comm = "python -m gutenberg.cleanup.strip_headers " + raw_path + " " + clean_path
        print clean_comm
        os.system(clean_comm)

if __name__=='__main__':
    clean()
