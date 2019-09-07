import requests
from django.shortcuts import render, redirect
import datetime
from .models import City
from .forms import CityForm

current_weather_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=AddYourOwnApiKey'
five_day_forecast_url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=AddYourOwnApiKey'

def index(request):
  city = 'Helsinki'
  form = CityForm()

  r = requests.get(current_weather_url.format(city)).json()
  r2 = requests.get(five_day_forecast_url.format(city)).json()

  city_weather = {
    'city': city,
    'temperature': r['main']['temp'],
    'description': r['weather'][0]['description'],
    'icon': r['weather'][0]['icon'],
  }
  five_day_forecast = r2['list']

  context = {
    'city_weather': city_weather, 
    'five_day_forecast': five_day_forecast,
    'form': form,
  }
  return render(request, 'weather/weather.html', context)


def search(request):
  if request.method == 'POST':
    form = CityForm(request.POST)
    if form.is_valid():
      city = form.cleaned_data['name']
      if requests.get(current_weather_url.format(city)).json()['cod'] == 200:
        r = requests.get(current_weather_url.format(city)).json()
        r2 = requests.get(five_day_forecast_url.format(city)).json()
        city_weather = {
          'city': city,
          'temperature': r['main']['temp'],
          'description': r['weather'][0]['description'],
          'icon': r['weather'][0]['icon'],
        }
        five_day_forecast = r2['list']
        form = CityForm
        context = {
          'city_weather': city_weather, 
          'five_day_forecast': five_day_forecast,
          'form': form,
        }
        return render(request, 'weather/weather.html', context)
      else:
        city = 'Helsinki'
        form = CityForm
        context = {
          'city_weather': '', 
          'five_day_forecast': '',
          'form': form,
          'err_msg': 'City not found'
        }
        return render(request, 'weather/weather.html', context)


