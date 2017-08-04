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
            remote_data = p.fetch_remote_data()
            if remote_data is None:
                continue

            d = remote_data.data # hace el save
            formato = p.file_format
            f = open(STATIC_OPENDATA_ROOT + '/data/'+nombre.replace(" ", "_").lower()+'-'+str(now)+'.'+formato, 'w+')
            f.write(d)