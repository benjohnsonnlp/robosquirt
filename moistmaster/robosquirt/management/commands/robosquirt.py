from django.core.management.base import BaseCommand

from robosquirt.server import main


class Command(BaseCommand):

    help = 'Run the robosquirt server'

    def handle(self, *args, **options):
        main()

