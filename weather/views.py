import requests
from django.shortcuts import render

from .models import City
from .forms import CityForm

def index(request):
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&&units=imperial&APPID=40c37c39e51a16b9d5f7ad46a1219f12'

    form = CityForm()

    cities = City.objects.all()
    weather_data = {}

    db_dict = []
    for city in cities:
        r = requests.get(url.format(city)).json()
        d = {
            'city':city.name,
            'temperature': r['main']['temp'],
            'description':r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        db_dict.append(d)
        weather_data.update({'db_dict': db_dict})

    if request.method == 'POST':
        city = request.POST.get('name', '')
        r = requests.get(url.format(city)).json()
        user_dict = []
        u = {
            'city': city,
            'temperature': r['main']['temp'],
            'description':r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }
        user_dict.append(u)
        weather_data.update({'user_dict':user_dict})
        context = {'city_weather': weather_data, 'form': form}

        return render(request, 'weather/weather.html', context)

    if request.method == 'GET':
        context = {'city_weather': weather_data, 'form': form}

        return render(request, 'weather/weather.html', context)
