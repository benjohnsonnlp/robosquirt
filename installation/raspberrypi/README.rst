Install Robosquirt on a Raspberry PI
=====================================

Run the ``install.sh`` script as root. It's as simple as that!


What the script does
--------------------

1. Creates a ``var/apps/`` directory owned by the standard ``pi`` user/group.
2. Checks out the Github project into ``var/apps/robosquirt``.
3. Adds Systemd service definition files for robosquirt and moistmaster
4. Adds rsyslog configuration for both services. Their logs will show up in ``/var/log/robosquirt.log`` and ``/var/log/moistmaster.log``, respectively.

The only thing you need to do now is create the database and load necessary data with::

    ./manage.pt migrate
    ./manage.pt setup

To run robosquirt::

    sudo systemctl start robosquirt

To run moistmaster::

    sudo systemctl start moistmaster

