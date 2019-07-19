import logging
from pathlib import Path
import subprocess

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from geo.models import UserSettings


class Command(BaseCommand):

    help = 'Setup the Moistmaster Django app'
    logger = logging.getLogger("robosquirt")
    data_file = Path(settings.BASE_DIR, "bundled_data", "USGS-GNIS-locations-2019-20190501.sql.gz")
    sqlite_db = Path(settings.BASE_DIR, "..", "robosquirt.db")

    def setup_user_stuff(self):
        try:
            User.objects.get()
        except User.DoesNotExist:
            User.objects.create_user(settings.DEFAULT_USERNAME)
            logging.info("Created default user.")
        UserSettings.objects.get_or_create()

    def load_location_data(self):
        self.logger.info("Loading location data. This may take a few minutes...")
        sql_stream = subprocess.Popen(("gunzip", "--stdout", str(self.data_file)), stdout=subprocess.PIPE)
        subprocess.check_output(("sqlite3", str(self.sqlite_db)), stdin=sql_stream.stdout)
        sql_stream.wait()
        self.logger.info("Locations loaded.")

    def handle(self, *args, **options):
        self.setup_user_stuff()
        self.load_location_data()
        self.logger.info("Setup complete.")

