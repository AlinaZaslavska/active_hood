from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from django.contrib.auth.models import User
from events.models import Event
from events.serializers import EventSerializer
from events.forms import EventForm

class CreateEventTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.valid_payload = {
            'name': 'yoga',
            'description': 'Yoga in the park',
            'date': '2024-07-19T10:00:00Z',
            'location': 1  # Assuming you have a City object with id 1
        }
        self.invalid_payload = {
            'name': '',
            'description': 'Yoga in the park',
            'date': '2024-07-19T10:00:00Z',
            'location': 1
        }

    @patch('events.forms.EventForm.is_valid')
    @patch('events.forms.EventForm.save')
    def test_create_event_valid_data(self, mock_save, mock_is_valid):
        mock_is_valid.return_value = True
        mock_event = Event(name='yoga', description='Yoga in the park', date='2024-07-19T10:00:00Z', location_id=1, creator=self.user)
        mock_save.return_value = mock_event

        response = self.client.post(reverse('create_event'), data=self.valid_payload, format='json')
        event = Event.objects.get()
        serializer = EventSerializer(event)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    @patch('events.forms.EventForm.is_valid')
    def test_create_event_invalid_data(self, mock_is_valid):
        mock_is_valid.return_value = False
        response = self.client.post(reverse('create_event'), data=self.invalid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)