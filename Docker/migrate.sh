#!/bin/bash
sleep 2
python3 run.py db init
python3 run.py db migrate
python3 run.py db upgrade
python3 run.py
