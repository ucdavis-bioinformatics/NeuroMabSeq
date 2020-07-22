# NeuroMabSeq Website

## DJANGO + NGINX + GUNICORN  see the tutorial for setup below.

### TODO:
- 101.1 101.2 etc if repeats..

### 2.0 
- how to backup sql lite database
- definitions from a file
- Rsync with ssh credentials for sam
- play with blat
    - https://genome.ucsc.edu/goldenpath/help/blatSpec.html
- nginx prefix edit 
- admin login and admin logout
- debug=FALSE, turn of debug, any other steps to check for proper deployment settings
- status page improvements
- finish duplicates links (not wanted?)
- automate index to see what files need to be added still
- csv download option for a specific query.. allow users to do more with the data like get fasta files etc...
- no loading libraries from internet have static files
- some views https with login.. no cert long term
- each time database is reloaded the id in url changes, make this static for them all somehow (still some work to do on this)


### Meeting notes
- check with cutoff from sam, p5
- create some stats for the subclone groupings? API with sequence->phylogeneitc tree?
- 5 subclones of the same parent should be identical?
- see what is feasible for rules for ^^ highlight things that are similar and see if they are similar
- upload the whole plate? Pull duplicates first?
- worth quantifying RNA, amplicons or new RNA for failures...
- if RNA there then try different protocol > cDNA from everything
- auto detect query
- work with the addgene metadata 
- moving into parents.. flexibility trial period another 4000 sequences 
- abberant.. screws things up (oligoclonal, monoclonal,subclones)
- mass spec to test things.. antibody have some characteristics 
- fancy machine for liquid transfer needs more work done on it 
- endpoint analysis. rtPCR. mass genotyping of crops is same technology for covid testing

 


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
       

  
#### This will fix 99% of problems unless someone pushes something funny to the repo!!!!
```  # from the Neuromabseq directory
sudo pkill gunicorn   
git fetch --all
git reset --hard origin/website
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
```
