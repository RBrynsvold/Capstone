1. Clone the nlp-research-box-rambo repo

        ```git clone https://github.com/terminal-labs/nlp-research-box-rambo.git```

2. In your clone of the nlp-research-box-rambo, navigate to **INSTALL.md** (linked at the top of the README page) and follow the instructions there.

   This will produce an exact replica of the environment used to do this data science work, fully contained inside a virtual machine.  All of the remaining steps are to be performed inside your rambo vm.

3. Clone this repo at the root level of your vm (/home/vagrant)

        ```git clone https://github.com/RBrynsvold/Capstone.git /home/vagrant```
        
4. Download the cleaned data from the public mirror repo

        ```bash /home/vagrant/Capstone/bash_scripts/wget_download_from_mirror.sh```
        
5. Execute the dimensional reduction script
        ```python /home/vagrant/Capstone/bash_scripts/dim_reduction_corp_class.py```
  
  **Rachel's self-reminder note - change script name for final**
5. Execute the lda fitting script
6. Inspect the results of your fitted model inside a jupyter notebook!
   **to be added: the jupyter tunneling instructons**
