# your_app/tests.py

from django.test import TestCase, RequestFactory
from django.urls import reverse
from locations.models import Bundesland, City
from locations.views import load_cities  # Adjust as per your actual app name

class AjaxLoadCitiesTestCase(TestCase):
    def setUp(self):
        # Create Bundesland
        self.bundesland = Bundesland.objects.create(name='Example Bundesland')

        # Create Cities
        self.city1 = City.objects.create(name='City 1', bundesland=self.bundesland)
        self.city2 = City.objects.create(name='City 2', bundesland=self.bundesland)

        self.factory = RequestFactory()

    def test_load_cities(self):
        url = reverse('locations:load_cities')  # Adjust URL name as per your project
        request = self.factory.get(url, {'bundesland_id': self.bundesland.pk})
        response = load_cities(request)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {'cities': [{'id': self.city1.pk, 'name': 'City 1'}, {'id': self.city2.pk, 'name': 'City 2'}]})
