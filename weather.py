import sys
import requests
from datetime import datetime
from dateutil import parser
import pprint as pp
import configparser
import logging

logger = logging.getLogger()
config = configparser.ConfigParser()
config.read('weather.ini')
GOOGLE_API_KEY = config.get('DEFAULT', 'GOOGLE_API_KEY', fallback=None)
logger.info("Using Google API key: %s" %GOOGLE_API_KEY)

def get_weather_report_for_today(latitude, longitude):
    weather_report = {}
    today = datetime.now().astimezone().strftime('%Y-%m-%d')
    full_report = get_weather_report(latitude, longitude)
    weather_report['meta'] = full_report['meta']
    if today in full_report:
        weather_report[today] = full_report[today]
    return weather_report

def get_weather_report_for(latitude, longitude, date):
    weather_report = {}
    full_report = get_weather_report(latitude, longitude)
    weather_report['meta'] = full_report['meta']
    if date in full_report:
        weather_report[date] = full_report[date]
    return weather_report

def get_weather_report(latitude, longitude):
    today = datetime.now().astimezone()
    weather_report = {
        'meta': {
            'time_of_report': today.strftime("%Y-%m-%d %H:%M:%S %Z"),
            'timezone': today.strftime('%Z'),
            'latitude': latitude,
            'longitude': longitude
        }
    }
    # Get the weather data from api.weather.gov
    url = f"https://api.weather.gov/points/{latitude},{longitude}"
    resp = requests.get(url)
    url = resp.json()['properties']['forecastGridData']
    resp = requests.get(url)
    # Reorganize the data into a JSON of our liking
    # Another way of saying this is that we're restructuring the data
    temp_data = resp.json()['properties']['temperature']
    dew_data = resp.json()['properties']['dewpoint']
    relhum_data = resp.json()['properties']['relativeHumidity']
    rain_data = resp.json()['properties']['probabilityOfPrecipitation']
    weather_data = resp.json()['properties']['weather']
    windchill_data = resp.json()['properties']['windChill']
    windspeed_data = resp.json()['properties']['windSpeed']
    windspeed_uom = parse_uom(windspeed_data['uom'])
    winddirection_data = resp.json()['properties']['windDirection']
    winddirection_uom = parse_uom(winddirection_data['uom'])
    for reading in temp_data['values']:
        time_data = parse_valid_time(reading['validTime'])
        date = time_data['date']
        time = time_data['time']
        prepare_entry(weather_report, date, time)
        if reading['value']:
            weather_report[date][time]['temp']['celsius'] = round(reading['value'], 1)
            weather_report[date][time]['temp']['fahrenheit'] = celsius_to_fahrenheit(reading['value'])
            weather_report[date][time]['temp']['period'] = time_data['period']
    for reading in dew_data['values']:
        time_data = parse_valid_time(reading['validTime'])
        date = time_data['date']
        time = time_data['time']
        prepare_entry(weather_report, date, time)
        if reading['value']:
            weather_report[date][time]['dewpoint']['celsius'] = round(reading['value'], 1)
            weather_report[date][time]['dewpoint']['fahrenheit'] = celsius_to_fahrenheit(reading['value'])
            weather_report[date][time]['dewpoint']['period'] = time_data['period']
    for reading in relhum_data['values']:
        time_data = parse_valid_time(reading['validTime'])
        date = time_data['date']
        time = time_data['time']
        prepare_entry(weather_report, date, time)
        weather_report[date][time]['relative_humidity']['percent'] = reading['value']
        weather_report[date][time]['relative_humidity']['period'] = time_data['period']
    for reading in rain_data['values']:
        time_data = parse_valid_time(reading['validTime'])
        date = time_data['date']
        time = time_data['time']
        prepare_entry(weather_report, date, time)
        weather_report[date][time]['chance_of_rain']['percent'] = reading['value']
        weather_report[date][time]['chance_of_rain']['period'] = time_data['period']
    for reading in weather_data['values']:
        time_data = parse_valid_time(reading['validTime'])
        date = time_data['date']
        time = time_data['time']
        prepare_entry(weather_report, date, time)
        weather_report[date][time]['weather']['period'] = time_data['period']
        for value in reading['value']:
            description = {
                'weather': value['weather'],
                'coverage': value['coverage'],
                'intensity': value['intensity']
            }
            weather_report[date][time]['weather']['description'].append(description)
    for reading in windchill_data['values']:
        time_data = parse_valid_time(reading['validTime'])
        date = time_data['date']
        time = time_data['time']
        prepare_entry(weather_report, date, time)
        if reading['value']:
            weather_report[date][time]['wind_chill']['celsius'] = round(reading['value'], 1)
            weather_report[date][time]['wind_chill']['fahrenheit'] = celsius_to_fahrenheit(reading['value'])
            weather_report[date][time]['wind_chill']['period'] = time_data['period']
    for reading in windspeed_data['values']:
        time_data = parse_valid_time(reading['validTime'])
        date = time_data['date']
        time = time_data['time']
        prepare_entry(weather_report, date, time)
        if reading['value']:
            weather_report[date][time]['wind_speed']['uom'] = windspeed_uom
            weather_report[date][time]['wind_speed']['speed'] = round(reading['value'], 3)
            weather_report[date][time]['wind_speed']['period'] = time_data['period']
    for reading in winddirection_data['values']:
        time_data = parse_valid_time(reading['validTime'])
        date = time_data['date']
        time = time_data['time']
        prepare_entry(weather_report, date, time)
        if reading['value']:
            weather_report[date][time]['wind_direction']['uom'] = winddirection_uom
            weather_report[date][time]['wind_direction']['angle'] = reading['value']
            weather_report[date][time]['wind_direction']['period'] = time_data['period']
    return weather_report

def prepare_entry(weather_report, date, time):
    if date not in weather_report:
        weather_report[date] = {}
    if time not in weather_report[date]:
        weather_report[date][time] = {
            'temp': {
                'celsius': None,
                'fahrenheit': None,
                'period': None
            }, 
            'dewpoint': {
                'celsius': None,
                'fahrenheit': None,
                'period': None
            },
            'relative_humidity': {
                'percent': None,
                'period': None
            },
            'chance_of_rain': {
                'percent': None,
                'period': None
            },
            'weather': {
                'description': [],
                'period': None
            },
            'wind_chill': {
                'celsius': None,
                'fahrenheit': None,
                'period': None
            },
            'wind_speed': {
                'uom': None,
                'speed': None,
                'period': None
            },
            'wind_direction': {
                'uom': None,
                'angle': None,
                'period': None
            }
        }

def parse_valid_time(valid_time):
    dt = valid_time.split("/")[0]
    dt = parser.parse(dt).astimezone()
    return {
        'date': dt.strftime("%Y-%m-%d"),
        'time': dt.strftime("%H:%M:%S"),
        'period': valid_time.split("/")[1].replace('P', '').replace('T', '')
    }

def celsius_to_fahrenheit(celsius):
    return celsius * 1.8 + 32

def parse_uom(uom):
    if uom == 'wmoUnit:km_h-1':
        return 'km/h'
    if uom == 'wmoUnit:degree_(angle)':
        return 'degrees'
    return None

def geocode(address):
    if not GOOGLE_API_KEY:
        logger.info("A GOOGLE_API_KEY is needed in the weather.ini file")
        return
    try:
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_API_KEY}"
        resp = requests.get(url)
        data = resp.json()
        if data['status'] == 'OK' and len(data['results']) > 0:
            return {
                'address': data['results'][0]['formatted_address'],
                'latitude': data['results'][0]['geometry']['location']['lat'],
                'longitude': data['results'][0]['geometry']['location']['lng']
            }
    except:
        logger.error("Error calling the Google Geocoding API web service")
    return None

def main():
    if len(sys.argv) < 3:
        print("Usage: python %s <latitude> <longitude>" %sys.argv[0])
        return
    latitude = float(sys.argv[1])
    longitude = float(sys.argv[2])
    weather_report = get_weather_report_for_today(latitude, longitude)
    pp.pprint(weather_report)

if __name__ == '__main__':
    main()