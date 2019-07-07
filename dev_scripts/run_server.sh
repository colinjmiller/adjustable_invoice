#!/bin/sh

# Give postgres a few seconds to finish starting
sleep 5

# Recreate the DB on each start
python manage.py recreate_db
python manage.py db upgrade

# Add all of the sample line items
python manage.py import_line_items

# And aaaway we go!
flask run --host=0.0.0.0
