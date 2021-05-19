import requests
import configparser
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def weather_dashboard():
    return render_template('home.html')


@app.route('/results', methods=['POST'])
def render_results():
    zip_code = request.form['zipCode']

    api_key = get_api_key()
    data = get_weather_results(zip_code, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"]) #formatted as a string with 2 decimals
    feels_like = "{0:.2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]
    wind_speed = data["wind"]["speed"]
    wind_direction = data["wind"]["deg"]
    wind_gust = data["wind"]["gust"]
    air_pressure = data["main"]["pressure"]


    return render_template('results.html',
                           location=location, wind_direction=wind_direction, wind_speed=wind_speed,
                           wind_gust=wind_gust, air_pressure=air_pressure) #association between variables parased and html
def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results(zip_code, api_key):
    api_url = "http://api.openweathermap.org/" \
              "data/2.5/weather?q={}&units=metric&appid={}".format(zip_code, api_key)
    r = requests.get(api_url)
    print(r.json())
    return r.json()


if __name__ == '__main__':
    app.run()