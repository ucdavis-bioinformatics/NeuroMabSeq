NeuroMabSeq

1. Check out the Django Project Tutorial in this directory.
- This will cover:
    - setting up a local development version
        - conda, mysqldb, etc. 
2. Setting Up the AWS instance (Ubuntu 18.04)
    - ssh onto the instance (see private instructions) for the key and doing this in AWS
    -Setup of Mysql:
     ```
     sudo apt update
     sudo apt install mysql-server
     sudo mysql
     mysql> create database trimmer_lab;
     ```
    - Setup of the conda:
        ```
        cd /tmp
        curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
        bash Anaconda3-2019.03-Linux-x86_64.sh
        ```
      Yes ,yes ,yes enter etc. 
        `source ~/.bashrc`
   
    - Setup the Repo
        ```
        git clone trimmer_lab_repo  TODO
        ```
    - Setup of the conda env:
        ```
        conda create --name trimmer_lab --file requirements.txt 
        ```