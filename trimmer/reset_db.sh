./manage.py shell < wipe_db.py
./manage.py shell < wipe_status_data.py
rm mydatabase
#python manage.py makemigrations
python manage.py migrate
# directory, update True/False (False will run a reset)
./manage.py shell < run_update.py
./manage.py shell < run_status_update.py
./manage.py shell < run_metadata_update.py
./manage.py shell < generate_blat.py
./manage.py shell < upload_faq.py