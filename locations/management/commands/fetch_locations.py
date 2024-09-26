import requests
from django.core.management.base import BaseCommand
from locations.models import City
from decouple import config
from locations.models import Bundesland, City

GEONAMES_USERNAME = config('GEONAMES_USERNAME')  # Replace with your Geonames username



class Command(BaseCommand):
    help = 'Fetch and store Bundesland and City data from Geonames'

    def handle(self, *args, **kwargs):
        # Fetch Bundesland data
        bundesland_url = f'http://api.geonames.org/childrenJSON?geonameId=2921044&username={GEONAMES_USERNAME}'
        bundesland_response = requests.get(bundesland_url)

        if bundesland_response.status_code == 200:
            bundesland_data = bundesland_response.json().get('geonames', [])
            for bundesland in bundesland_data:
                bundesland_name = bundesland['name']
                bundesland_obj, created = Bundesland.objects.get_or_create(name=bundesland_name)
                self.stdout.write(self.style.SUCCESS(f'Successfully created Bundesland: {bundesland_name}'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch Bundesland data'))

        # Fetch City data
        city_url = f'http://api.geonames.org/searchJSON?country=DE&maxRows=1000&username={GEONAMES_USERNAME}'
        city_response = requests.get(city_url)

        if city_response.status_code == 200:
            city_data = city_response.json().get('geonames', [])
            for city in city_data:
                city_name = city['name']
                bundesland_name = city.get('adminName1', '')
                if bundesland_name:
                    bundesland_obj = Bundesland.objects.filter(name=bundesland_name).first()
                    if bundesland_obj:
                        City.objects.get_or_create(name=city_name, bundesland=bundesland_obj)
                        self.stdout.write(self.style.SUCCESS(f'Successfully created City: {city_name} in {bundesland_name}'))
                    else:
                        self.stdout.write(self.style.ERROR(f'Bundesland {bundesland_name} not found for city {city_name}'))
                else:
                    self.stdout.write(self.style.ERROR(f'No Bundesland found for city {city_name}'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch City data'))