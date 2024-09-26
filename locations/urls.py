from django.urls import path
from locations.views import load_cities

app_name = 'locations'  # Namespace for the app

urlpatterns = [
    path('ajax/load-cities/',load_cities, name='load_cities'), # AJAX
]
