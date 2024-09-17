#!/bin/sh
python3 scripts/add_constants.py
python3 scripts/analyse.py
python3 scripts/filter.py
xdg-open final.csv
