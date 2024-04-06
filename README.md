# NeuroMabSeq Website

## Just the website and database code install



## Just the pipeline install



## DJANGO + NGINX + GUNICORN  see the tutorial for setup below.


1. Check out the Django Project Tutorial in this directory.
    - This will cover: (Look at files on the instance AMI for reference specifically NGINX.conf and Gunicorn.conf files)       
    - `https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04`
    
2. Setting Up the AWS instance and Mysql (Ubuntu 18.04)
    - ssh onto the instance (see private instructions) for the key and doing this in AWS
    -Setup of Mysql (no longer needed.. uses sqllite): 
         ```
         sudo apt update
         sudo apt install mysql-server
         sudo mysql
         mysql> create database trimmer_lab;
         ```
    - `sudo apt-get install mysql-devel` (No longer needed, uses sqllite)
   
    - Django will want to connect using root user with no password to a local db.
        ```
        use mysql;
        update user set authentication_string=password(''), plugin='mysql_native_password' where user='root';
        ```
3. Conda setup
    - Setup of the conda:
        ```
        cd /tmp
        curl -O https://repo.anaconda.com/archive/Anaconda3-2019.03-Linux-x86_64.sh
        bash Anaconda3-2019.03-Linux-x86_64.sh
        ```
      Yes ,yes ,yes enter etc. 
        `source ~/.bashrc`
   - Setup of the conda env:
        ```
        conda env create --name trimmer_lab --file environment.yml
        source activate trimmer_lab
        ```
4. Repo setup 
    - Setup the Repo
        ```
        git clone --single-branch --branch website https://github.com/ucdavis-bioinformatics/NeuroMabSeq.git
        ```
    - `sudo apt-get install gcc`

   - Run `python manage.py runserver` and see if it works along with `python manage.py migrate`, and `python manage shell`
       

5. Cert setup: `https://certbot.eff.org/lets-encrypt/ubuntubionic-nginx`
6. Adding users: `https://aws.amazon.com/premiumsupport/knowledge-center/new-user-accounts-linux-instance/` (just steps)
7. Custom fasta renderer: `https://www.django-rest-framework.org/api-guide/renderers/#custom-renderers`




#### This will fix 99% of problems unless someone pushes something funny to the repo
```  # from the Neuromabseq directory

sudo pkill gunicorn   
git fetch --all
git reset --hard origin/website_2.0
cd trimmer
python manage.py migrate
sudo systemctl restart gunicorn
sudo systemctl restart nginx
psudo python manage.py collectstatic
```

#### This will fix 99% of problems but will not update the repo
```
sudo pkill gunicorn   
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

#### Resetting the database: (see methods.py) need to make this stable for a login though (see `./reset_db.sh`)
```
./manage.py shell < wipe_db.py
./manage.py shell < wipe_status_data.py
rm mydatabase
python manage.py migrate
./manage.py shell < run_update.py
./manage.py shell < run_status_update.py
./manage.py shell < run_metadata_update.py
./manage.py shell < run_metadata_update.py
```
