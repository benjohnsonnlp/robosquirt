##########
Robosquirt
##########

Software to power a garden watering solution.


To get started::

    pip install -r requirements/dev.txt
    cd moistmaster && ./manage.py migrate && ./manage.py setup


You'll want to run both the robosquirt server, which controls the valves::

    ./manage.py robosquirt


As well as "moist master", the web-based controller::

    ./manage.py runserver

