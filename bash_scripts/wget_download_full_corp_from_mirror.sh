#this one worked in my most recent run
cd /data/ProjectGutenberg
wget -r -nd --no-parent http://54.187.164.38:5000/clean_books -P full_corp_28k
cd -

#old script for reference - delete after confirmation
#wget -r -nd --no-parent http://54.187.164.38:5000/full_corp_28k/clean_books -P full_corp_28k
