#!/bin/sh

# Exit immediately if anything fails
set -e

# Run static analysis on the project
# Note: Ignore E402, enforcing imports at top of file. Often it's cleaner to
# import where it is necessary, such as in adjustable_invoice/__init__py.
pycodestyle adjustable_invoice/ --ignore=E402

echo "PEP8 analysis passed. Proceeding to unit tests."

# Give postgres a few seconds to finish starting
sleep 5

# Recreate the DB on each start
python manage.py recreate_db
python manage.py db upgrade

# Add all of the sample line items
python manage.py import_line_items

pytest

echo "All tests passed!"
