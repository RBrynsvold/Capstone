1. Clone the nlp-research-box-rambo repo
               
               git clone https://github.com/terminal-labs/nlp-research-box-rambo.git



2. In your clone of the nlp-research-box-rambo, navigate to **INSTALL.md** (linked at the top of the README page) and follow the instructions there.

   This will produce an exact replica of the environment used to do this data science work, fully contained inside a virtual machine.  Steps 3-6 are to be performed inside your rambo vm.


3. Clone or fork this repo on your vm at /home/vagrant (note this is the default working directory when you ssh in)

                git clone https://github.com/RBrynsvold/Capstone.git
        
   _Clone if you want to reproduce the work, fork if you want to do some coding of your own and further explore this data set!_


4. Download the cleaned data from the public mirror repo

                bash /home/vagrant/Capstone/bash_scripts/wget_download_from_mirror.sh
 
 
5. Execute the dimensional reduction script

   For this step you must enter the Capstone/py_scripts directory:
   
                cd /home/vagrant/Capstone/py_scripts
     
   Then you can run the script:

                python dim_reduction_corp_class.py
   **REMINDER - change script name for final**
   
   Note: you will be prompted to provide an identifier string for your run.


6. Execute the lda modeling script (also from the py_scripts directory)

                python fit_gensim_lda.py

   You will be prompted for the following information:
   
      * The identifier string for the corpus and dictionary from which to build the model
        __This string must match exactly the string given in step 5!__
      * Number of topics to use for model fitting
        __In this project I determined the optimal number of topics to be NUMBERISTBD__
      * Number of cores on your machine
        If greater than 1, the model will be run multithreaded
        
   Depending on the details of your vm, this step will take several hours at least.

7. Inspect the results of your fitted model inside a jupyter notebook!

   Your rambo vm should be set up such that you can easily tunnel in with a jupyter notebook, run from a browser on your computer.  Steps:
   
   * Determine your public IP address ('IPv4 Public IP') by viewing it on your aws EC2 console
   * Open a browser window and enter your your IPv4 Public IP, followed by ':8080'
   
      <yourIPv4PublicIP>:8080
      
   * Enter 'admin' in the password field
   * Navigate into the Capstone/notebooks directory
   * Open the 'load_inspect_model.ipynb' notebook
   * Execute the cells in order and make your own conclusions!
