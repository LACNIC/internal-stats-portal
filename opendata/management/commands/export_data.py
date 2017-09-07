from django.core.management.base import BaseCommand
from core.models import Publication, Data
# from app.static_defs import NOISY_PREFIXES
# import csv
import json
import datetime
import pytz
from internal_stats_portal.settings import STATIC_OPENDATA_ROOT


class Command(BaseCommand):
    def handle(self, *args, **options):
        now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc).date()
        publications = Publication.objects.all()

        for p in publications:
            nombre = p.name
            remote_data = p.fetch_remote_data()  # hace el save de un nuevo Data
            if remote_data is None:
                continue

            d = remote_data.data
            formato = p.file_format
            f = open(STATIC_OPENDATA_ROOT + '/data/' + p.get_filename() + '-' + str(now) + '.' + formato, 'w+')
            f.write(d)
            f.close()

            # Generate the 'latest' version
            g = open(STATIC_OPENDATA_ROOT + '/data/' + p.get_filename() + '-' + 'latest' + '.' + formato, 'w+')
            g.write(d)
            g.close()
