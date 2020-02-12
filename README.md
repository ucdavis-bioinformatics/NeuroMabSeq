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
        git clone --single-branch --branch website https://github.com/ucdavis-bioinformatics/NeuroMabSeq.git
   
        ```
    - `sudo apt-get install gcc`
    - `sudo apt-get install mysql-devel`
   
    - Setup of the conda env:
        ```
        conda env create --name trimmer_lab --file environment_linux.yml
        source activate trimmer_lab
        ```
    - Django will want to connect using root user with no password to a local db.
        ```
        use mysql;
        update user set authentication_string=password(''), plugin='mysql_native_password' where user='root';
        ```
   - Run `python manage.py runserver` and see if it works
   
   `python manage.py migrate`
   
   `python manage shell`
   
   `https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04