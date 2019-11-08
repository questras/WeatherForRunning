from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Weather

import datetime

EXISTING_CITY = 'London'
NOT_EXISTING_CITY = 'qqqqqqqqqqqq'
INDEX = 'Weather Forecast'


def create_weather():
    weather = Weather.objects.create(city=EXISTING_CITY)
    return weather


class WeatherTests(TestCase):
    # Test if city from database appears in list on index page
    def test_last_searched_appears(self):
        w = create_weather()
        response = self.client.get(reverse('index'))
        self.assertContains(response, w.city)

    def test_no_last_searched(self):
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, 'cityButton')

    # Test if searching for city directs to page with this city
    def test_search_for_existing_city(self):
        response = self.client.post(reverse('search'), {'city': EXISTING_CITY})
        self.assertContains(response, EXISTING_CITY)

    def test_search_for_not_existing_city(self):
        response = self.client.post(reverse('search'), {'city': NOT_EXISTING_CITY})
        # 302 is redirect status code
        self.assertEquals(response.status_code, 302)
