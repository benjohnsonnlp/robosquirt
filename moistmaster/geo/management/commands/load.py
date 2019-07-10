from django.core.management.base import BaseCommand, CommandError
from pathlib import Path

from geo.load import GNISLoader


class Command(BaseCommand):

    """
    Files can be downloaded from:
    https://www.usgs.gov/core-science-systems/ngp/board-on-geographic-names/download-gnis-data
    """

    help = 'Load USGS place names data file.'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        path = Path(options["file"]).expanduser().resolve()
        if not path.is_file():
            raise CommandError('File "{}" does not exist'.format(path))
        loader = GNISLoader(path)
        loader.load()
