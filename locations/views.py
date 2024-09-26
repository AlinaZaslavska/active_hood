from django.http import JsonResponse
from locations.models import Bundesland, City
from django.shortcuts import render


def load_cities(request):

    bundesland_id = request.GET.get('bundesland_id')
    print( bundesland_id)
    cities = City.objects.filter(bundesland_id=bundesland_id).order_by('name')
    print(cities)
    return JsonResponse({'cities': [{'id': city.id, 'name': city.name} for city in cities]})