import requests
import os
from dotenv import load_dotenv
import re

load_dotenv('../.env')


def get_weather(city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    w_params = {"q": city, "appid": os.environ.get("API_key_openweathermap")}
    w = requests.get(base_url, params=w_params)
    return w.json()


if __name__ == "__main__":
    city = input("Введите название города на английском языке ")
    w = get_weather(city)
    print(f"Температура в городе {city} равна {round(w['main']['temp'] - 273)} градусам по цельсию \n"
          f"Скорость ветра {round(w['wind']['speed'])} м/с")
