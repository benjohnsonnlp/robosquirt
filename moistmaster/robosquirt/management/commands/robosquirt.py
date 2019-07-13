import logging

from django.core.management.base import BaseCommand

from robosquirt.server import main


class Command(BaseCommand):

    help = 'Run the robosquirt server'
    logger = logging.getLogger("robosquirt")

    def handle(self, *args, **options):
        self.logger.info("Starting robosquirt server...")
        main()
