# core/utils.py
import requests
import math

API_KEY = 'AIzaSyDq4hfFdWYgcnVpxU1nd7dLrn4N9au6Mt4'

def get_coordinates(address):
    response = requests.get(
        'https://maps.googleapis.com/maps/api/geocode/json',
        params={'address': address, 'key': API_KEY}
    )
    results = response.json().get('results')
    if not results:
        return None, None
    location = results[0]['geometry']['location']
    return location['lat'], location['lng']

def get_distance_driving(origin, destination):
    response = requests.get(
        'https://maps.googleapis.com/maps/api/directions/json',
        params={
            'origin': origin,
            'destination': destination,
            'key': API_KEY,
            'mode': 'driving'
        }
    )
    routes = response.json().get('routes')
    if not routes:
        return None
    legs = routes[0]['legs']
    distance_meters = legs[0]['distance']['value']
    distance_km = distance_meters / 1000
    return distance_km

def calcular_frete(distancia):
    frete = distancia * 2 * 2 * 6 / 8
    # Arredondar para o próximo múltiplo de 5
    frete = math.ceil(frete / 5) * 5
    return frete
