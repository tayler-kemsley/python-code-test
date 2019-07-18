import logging

import requests
from django.conf import settings
from django.core.management import BaseCommand

from shiptrader.models import Starship

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def sanitise(self, data, remove_commas=False):
        if data.lower() == 'unknown':
            return None
        if remove_commas:
            return data.replace(',', '')
        return data


    def update_database(self, data):
        starship = Starship.objects.create(
            model=data['model'],
            starship_class=data['starship_class'],
            manufacturer=data['manufacturer'],

            # Potentially unknown data
            length=self.sanitise(data['length'], remove_commas=True),
            hyperdrive_rating=self.sanitise(data['hyperdrive_rating']),
            passengers=self.sanitise(data['passengers']),
            crew=self.sanitise(data['crew']),
            cargo_capacity=self.sanitise(data['cargo_capacity']),
        )
        logger.debug(
            'Starhip added: {} {}'.format(
                starship.starship_class, starship.manufacturer
            )
        )

        self.records_added += 1

    def handle(self, *args, **options):
        self.records_added = 0
        url = settings.SWAPI
        starship_endpoint = url + 'starships/?page=1'

        while True:
            print('QUERYING: {}'.format(starship_endpoint))
            results = requests.get(starship_endpoint).json()
            for result in results['results']:
                self.update_database(result)

            starship_endpoint = results['next']
            if not starship_endpoint:
                break

        self.stdout.write('Records added {}'.format(self.records_added))
