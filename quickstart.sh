#!/usr/bin/env bash
cd robosquirt
python3 -m robosquirt.server > ../squirt.log &
cd ../moistmaster/
./manage.py runserver 0.0.0.0:8080 > ../moist.log 2>&1 &
cd ..
