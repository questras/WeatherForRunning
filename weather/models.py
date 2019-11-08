from django.db import models
from django.utils import timezone


# Create your models here.


class Weather(models.Model):
    city = models.CharField(max_length=200)

    def __str__(self):
        return self.city

    def delete_obj(self):
        self.delete_obj()
