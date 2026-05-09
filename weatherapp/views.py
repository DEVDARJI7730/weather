from django.shortcuts import render
from django.contrib import messages
import requests
import datetime


def home(request):

    # Get city from form
    if request.method == "POST":
        city = request.POST.get('city')
    else:
        city = 'ahmedabad'

    # OpenWeather API Key
    WEATHER_API_KEY = '6b5410eeb2c00b2673f42af9489e2ff6'

    # Weather API URL
    weather_url = (
        f'https://api.openweathermap.org/data/2.5/weather'
        f'?q={city}&appid={WEATHER_API_KEY}&units=metric'
    )

    # Google Image API Keys (optional)
    API_KEY = ''
    SEARCH_ENGINE_ID = ''

    # Default image
    image_url = "wet.jpg"

    # ---------------- IMAGE SECTION ---------------- #

    # Only run if API keys exist
    if API_KEY and SEARCH_ENGINE_ID:

        query = city + " 1920x1080"

        city_url = (
            f"https://www.googleapis.com/customsearch/v1"
            f"?key={API_KEY}"
            f"&cx={SEARCH_ENGINE_ID}"
            f"&q={query}"
            f"&searchType=image"
            f"&imgSize=xlarge"
        )

        try:
            image_data = requests.get(city_url).json()

            search_items = image_data.get("items")

            if search_items and len(search_items) > 0:
                image_url = search_items[0]['link']

        except Exception:
            pass

    # ---------------- WEATHER SECTION ---------------- #

    try:

        response = requests.get(weather_url)

        data = response.json()

        print(data)

        if response.status_code != 200:
            raise KeyError

        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']

        day = datetime.date.today()

        context = {
            'description': description,
            'icon': icon,
            'temp': temp,
            'humidity': humidity,
            'pressure': pressure,
            'wind': wind,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        }

        return render(request, 'weatherapp/index.html', context)

    except Exception:

        messages.error(request, 'City information is not available to Weather API')

        day = datetime.date.today()

        context = {
            'description': 'Clear Sky',
            'icon': '01d',
            'temp': 25,
            'humidity': 50,
            'pressure': 1000,
            'wind': 2,
            'day': day,
            'city': 'Ahmedabad',
            'exception_occurred': True,
            'image_url': image_url
        }

        return render(request, 'weatherapp/index.html', context)