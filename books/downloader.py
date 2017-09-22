import sys, os, time

def downloads(num_list):

    path_head = "/Users/rachelbrynsvold/dsi/capstone_dir/top_100_dev_corp/books/"

    for n in num_list:
        raw_path = path_head + "raw/{}-raw.txt".format(n)
        clean_path =path_head + "clean/{}-clean.txt".format(n)

        downl_comm = "python -m gutenberg.acquire.text" + " " + str(n) + " " + raw_path
        print downl_comm
        os.system(downl_comm)

        clean_comm = "python -m gutenberg.cleanup.strip_headers " + raw_path + " " + clean_path
        print clean_comm
        os.system(clean_comm)

        time.sleep(5)

if __name__=='__main__':

    num_list = [33, 8800, 1080, 20, 521, 105, 730, 30601, 12, 932, 514, 108, 55404, 526, 38427, 203, 4517, 140, 21279]
    #[408, 28520, 2852, 10, 14264, 46, 863, 15399, 1322, 55387, 1727, 2680, 19942]
    #[160, 205, 36, 41, 45, 996, 1399, 33283, 2148, 236, 1112]
    #[161, 25305, 7370, 2174, 4363, 34901, 3600, 55]
    #[1404, 120, 224, 42, 100, 829, 28054]
    #[1260, 3207, 219, 147, 1497, 35, 768, 2814, 30360]
    #[174, 1184, 135, 20203, 844, 158]
    #[4300, 2500, 6130, 16, 1400, 23]
    #[2591, 74, 5200, 851, 2600]
    #[1661, 1232, 98, 16382, 345, 76, 84]
    downloads(num_list)
