#!/usr/bin/env sh
app=citation_manager
python manage.py dumpdata > temp_data.json
rm db.sqlite
python manage.py syncdb
python manage.py loaddata temp_data.json
# rm temp_data.json