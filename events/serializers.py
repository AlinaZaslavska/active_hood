from rest_framework import serializers
from events.models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'activity', 'description', 'date', 'location', 'participants']
        read_only_fields = ['creator']

