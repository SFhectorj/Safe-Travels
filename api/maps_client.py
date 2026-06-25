#Uses openroute api/ google map alternative

import os
import requests


BASE_URL = "https://api.openrouteservice.org"
DIRECTIONS_PROFILE = "foot-walking"


'''
takes in the name of the city 
Returns lon and lat of said city
'''
def geocode_city(name):
    api_key = os.getenv("ORS_API_KEY")
    
    url = f"{BASE_URL}/geocode/search"

    params = {
        "api_key": api_key,
        "text": name,
        "size": 1,
    }

    r = requests.get(url, params=params)
    
    

    data = r.json()
    feature = data["features"][0]
    lon, lat = feature["geometry"]["coordinates"]
    return lon, lat
'''
Takes in the start and end lon lat pair
returns the route
'''
def get_route(start, end):
    start_lon, start_lat = geocode_city(start)
    end_lon, end_lat = geocode_city(end)

    url = f"{BASE_URL}/v2/directions/{DIRECTIONS_PROFILE}/json"
    headers = {
        "Authorization": os.getenv("ORS_API_KEY"),
        "Content-Type": "application/json",
    }
    body = {
        "coordinates": [
        [start_lon,start_lat],
        [end_lon, end_lat],
        ]
    }

    r = requests.post(url, json=body,headers=headers)
    data = r.json()

    if "routes" not in data:
      raise ValueError(f"ORS error: {data}")
    
    route = data["routes"][0]
    summary = route["summary"]
    steps = route["segments"][0]["steps"]

    
    directions = []
    for step in steps:
        instruction = step["instruction"]          
        distance = step["distance"]                
        duration = step["duration"]                
        directions.append(
            f"{instruction} for {distance:.0f} m (~{duration/60:.1f} min)"
        )

    return {
        "distance_m": summary["distance"],
        "duration_s": summary["duration"],
        "geometry": route["geometry"],
        "directions": directions,
    }

def _get_route_via(start_lon, start_lat, mid_lon, mid_lat, end_lon, end_lat):
    url = f"{BASE_URL}/v2/directions/{DIRECTIONS_PROFILE}/json"
    headers = {
        "Authorization": os.getenv("ORS_API_KEY"),
        "Content-Type": "application/json",
    }
    body = {
        "coordinates": [
            [start_lon, start_lat],
            [mid_lon, mid_lat],
            [end_lon, end_lat],
        ]
    }
    r = requests.post(url, json=body, headers=headers)
    data = r.json()
    if "routes" not in data:
        return None
    route = data["routes"][0]
    summary = route["summary"]
    steps = route["segments"][0]["steps"]
    directions = [
        f"{s['instruction']} for {s['distance']:.0f} m (~{s['duration']/60:.1f} min)"
        for s in steps
    ]
    return {
        "distance_m": summary["distance"],
        "duration_s": summary["duration"],
        "geometry": route["geometry"],
        "directions": directions,
    }


def get_alternative_routes(start, end):
    start_lon, start_lat = geocode_city(start)
    end_lon, end_lat = geocode_city(end)

    mid_lon = (start_lon + end_lon) / 2
    mid_lat = (start_lat + end_lat) / 2

    route1 = get_route(start, end)

    route2 = _get_route_via(start_lon, start_lat, mid_lon, mid_lat + 0.012, end_lon, end_lat)
    route3 = _get_route_via(start_lon, start_lat, mid_lon, mid_lat - 0.012, end_lon, end_lat)

    routes = [route1]
    if route2:
        routes.append(route2)
    if route3:
        routes.append(route3)
    return routes