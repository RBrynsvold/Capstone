1. Clone the nlp-research-box-rambo repo

        git clone https://github.com/terminal-labs/nlp-research-box-rambo.git

2. In your clone of the nlp-research-box-rambo, navigate to **INSTALL.md** (linked at the top of the README page) and follow the instructions there.

   This will produce an exact replica of the environment used to do this data science work, fully contained inside a virtual machine.  Steps 3-5 are to be performed inside your rambo vm.

3. Clone or fork this repo on your vm at /home/vagrant (note this is the default working directory when you ssh in)

        git clone https://github.com/RBrynsvold/Capstone.git
        
   _Clone if you want to reproduce the work, fork if you want to do some coding of your own and further explore this data set!_
        
4. Download the cleaned data from the public mirror repo

        bash /home/vagrant/Capstone/bash_scripts/wget_download_from_mirror.sh
        
5. Execute the dimensional reduction script

        python /home/vagrant/Capstone/py_scripts/dim_reduction_corp_class.py
   **REMINDER - change script name for final**
   
5. Execute the lda modeling script

        python /home/vagrant/Capstone/py_scripts/fit_gensim_lda.py
        
6. Inspect the results of your fitted model inside a jupyter notebook!

   Your rambo vm should be setup for to easily tunnel in with a jupyter notebook, run on your computer.  Steps:
   
   * Determine your public ip address (IPv4)
   **to be added: the jupyter tunneling instructons**
