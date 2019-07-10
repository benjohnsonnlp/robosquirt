#!/usr/bin/env bash


cd moistmaster/
./manage.py robosquirt > ../robosquirt.log 2>&1 &
./manage.py runserver 0.0.0.0:8080 > ../moist.log 2>&1 &
