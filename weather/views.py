from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .models import Weather

import requests

API_CODE = '&APPID=7223a66ac88b0205f6fffbfefcd9df86'
API_URL = 'http://api.openweathermap.org/data/2.5/weather?q='


# # # # # # # # # # #
#  Helper functions #
# # # # # # # # # # #

# return string corresponding to question: is good for running?
def is_good_for_running(temperature, wind_speed):
    temperature = int(temperature)
    wind_speed = float(wind_speed)
    if temperature < -10:
        return "It's freezing. You better stay at home today."
    elif wind_speed > 25:
        return "It's really windy. You better stay at home today."
    elif -5 >= temperature >= -10:
        return "It's quite cold. You should consider going to the gym today."
    elif 10 >= temperature > -5:
        return "The weather is ok. You should go out running."
    else:
        return "The weather is very good. You should go out running."


# # # # #
# Views #
# # # # #


# Index view of the page
def index(request):
    # get all saved weathers from database
    weather_objects = Weather.objects.all()

    # create context for html file
    context = {'weather_objects': weather_objects}
    return render(request, 'weather/index.html', context=context)


def search(request):
    # get city name from search request
    city_name = request.POST.get('city').capitalize()

    # If no city in input, redirect to index page
    if not city_name:
        messages.warning(request, "Please, enter the city.")
        return HttpResponseRedirect(reverse('index'))

    # send get request to api
    api_request_url = API_URL + city_name + API_CODE
    api_request = requests.get(api_request_url)

    # if no city was found
    if api_request.status_code == 404:
        messages.warning(request, "There is no such city.")
        return HttpResponseRedirect(reverse('index'))

    # add the city to database with last searched
    if not Weather.objects.filter(city=city_name):
        Weather(city=city_name).save()

    # take request's json
    request_json = api_request.json()

    # take weather information
    city = request_json['name']
    clouding = request_json['weather'][0]['description']
    temperature = request_json['main']['temp']
    wind_speed = request_json['wind']['speed']

    # temperature is in Kelvins - convert to celsius
    temperature = str(int(temperature) - 273)
    # wind_speed is in m/s - convert to km/h
    wind_speed = str(round(float(wind_speed) * 3.6, 2))

    # get information if weather is good for running
    running_state = is_good_for_running(temperature, wind_speed)

    context = {
        'city': city,
        'clouding': clouding,
        'temperature': temperature,
        'wind_speed': wind_speed,
        'running_state': running_state,
    }

    return render(request, 'weather/weather.html', context=context)


def delete(request):
    id_to_be_deleted = int(request.POST['delete_button']) - 1
    weather_objects = Weather.objects.all()
    weather_obj = weather_objects[id_to_be_deleted]
    weather_obj.delete()

    return HttpResponseRedirect(reverse('index'))
