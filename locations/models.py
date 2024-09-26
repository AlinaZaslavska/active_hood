from django.db import models

class Bundesland(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    bundesland = models.ForeignKey(Bundesland, on_delete=models.CASCADE, related_name="city_set")
    def __str__(self):
        return self.name
    