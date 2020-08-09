./manage.py shell < wipe_db.py
./manage.py shell < wipe_status_data.py
rm mydatabase
python manage.py migrate
./manage.py shell < run_entry_reset.py
./manage.py shell < run_status_reset.py
./manage.py shell < run_metadata_update.py