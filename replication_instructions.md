1. Clone the nlp-research-box-rambo repo
               
               git clone https://github.com/terminal-labs/nlp-research-box-rambo.git

2. In your clone of the nlp-research-box-rambo, navigate to **INSTALL.md** (linked at the top of the README page) and follow the instructions there. 

   _A note on hardware requirements:  this project is intended to be run on a t2.xlarge EC2 or equivalent.  Note for more than 5 passes for the fitting script, you may want to use a more powerful machine/vm._

   This will produce an exact replica of the environment used to do this data science work, fully contained inside a virtual machine.  Steps 3-6 are to be performed inside your rambo vm.

3. Clone or fork this repo on your vm at /home/vagrant (note this is the default working directory when you ssh in)

                git clone https://github.com/RBrynsvold/Capstone.git
        
   _Clone if you want to reproduce the work, fork if you want to do some coding of your own and further explore this data set!_


4. Download the cleaned data from the public mirror repo

                bash /home/vagrant/Capstone/bash_scripts/wget_download_5k_from_mirror.sh
   
   _For advanced users, there is the option to download and model the full 28k-book corpus.  See notes at the bottom._
   
 
5. Set the run parameters for both scripts by tunneling in to the EC2 with a jupyter notebook

    Your rambo vm should be set up such that you can easily tunnel in with a jupyter notebook, run from a browser on your computer.  Steps:

    * Determine your public IP address ('IPv4 Public IP').   
        For an AWS EC2, you can find this by viewing it on your EC2 Management Console
    * Open a browser window and enter your your IPv4 Public IP, followed by ':8080'   
   
        _yourIPv4PublicIP_:8080
      
    * Enter 'admin' in the password field
    * Navigate into the Capstone/notebooks directory  
    * Launch the 'set_run_params.ipynb' notebook
    * Check all the numbers
    * **Enter a string to identify the dimensional reduction and make note of it for later**
    * Execute all cells.  
        _Defaults are given for parameter, but here is where you can tweak parameters for experimentation._ 


6. Execute the dimensional reduction script

   For this step you must enter the Capstone/py_scripts directory:
   
                cd /home/vagrant/Capstone/py_scripts
     
   Then you can run the script:

                python dimensional_reduction.py
   
   Note: you will be prompted to provide an identifier string for your run.  Use the same string you used in the set_run_params notebook.


7. Execute the lda modeling script (also from the py_scripts directory)

                python fit_gensim_lda.py

   You will be prompted for:
    * The identifier string for the corpus and dictionary from which to build the model       
          _**This string must match the string given in step 5!**_
    * An identifier string for the model
          _Can be different if desired_
        
   Depending on the details of your hardware, this step will take several minutes to several hours.

8. Inspect the results of your fitted model inside a jupyter notebook!
   
   * In your jupyter directory window (tunneling from step 5), open the 'load_inspect_model.ipynb' notebook
   * Execute the cells in order and do your own investigation of the results!
      
      
      
 **Note on Step 4:**   
_On the 5k-book corpus, the LDA algorithm will pretty consistently run to completion, but it is much more difficult (computationally intensive) to run on the full corpus.  Currently, I have not had success modeling the full corpus on a reasonably-priced EC2 instance like the t2.xlarge.  To download the full corpus, run this script instead of the one above:_

               bash /home/vagrant/Capstone/bash_scripts/wget_download_full_corp_from_mirror.sh
