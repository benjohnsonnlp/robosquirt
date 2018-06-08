cd robosquirt
python -m robosquirt.server > squirt.log &
cd ../moistmaster/
./manage.py runserver *:8080 2>&1 moist.log &
cd ..