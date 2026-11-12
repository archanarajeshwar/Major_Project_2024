import os
import requests
from geopy.geocoders import Nominatim

def gmaps(lat,long):
    api_key = os.environ.get("SERPAPI_API_KEY")
    if not api_key:
        raise RuntimeError("Set the SERPAPI_API_KEY environment variable before requesting map results.")
    query = 'hospitals|clinics'
    
    # latitude, longitude = geocode_address(address)
    link = f'https://serpapi.com/search.json?engine=google_maps&q={query}&ll=@{lat},{long},15.1z&type=search'
    params = {
    'key': api_key,
    }
    response = requests.get(link, params=params)
    addresses = dict(response.json())
    hospitals = addresses['local_results']
    hospital_data = []
    
    for i in range(len(hospitals)):        
        try:
            title = hospitals[i]['title']
        except:
            title = 'Not Specified'
        
        try:
            address = hospitals[i]['address']
        except:
            address = 'Not Specified'
            
        try:
            operating_days = [days for days in hospitals[i]['operating_hours']]
        except:
            operating_days = 'Not Specified'
        
        try:
            open_hours = hospitals[i]['open_state']
        except:
            open_hours = 'Not Specified'
            
        try:
            phone = hospitals[i]['phone']
        except:
            phone = 'Not Specified'
            
        try:
            type = hospitals[i]['type']
        except:
            type = 'Not Specified'
        
        try:
            reviews = hospitals[i]['reviews']
        except:
            reviews = 'Not Specified'
        
        try:
            rating = hospitals[i]['rating']
        except:
            rating = 'Not Specified'
            
        try:
            thumbnail = hospitals[i]['thumbnail']
        except:
            thumbnail = 'Not Specified'
        
        try:
            coordinates = hospitals[i]['gps_coordinates']
        except:
            coordinates = 'Not Specified'
        
        data = {
            'hospital_id': i,
            'name': title,
            'address': address,
            'days_open': operating_days,
            'open_time': open_hours,
            'contact': phone,
            'disease_treatment_type': type,
            'reviews': reviews,
            'rating': rating,
            'image': thumbnail,
            'coordinates': coordinates,
        }
        
        hospital_data.append(data)
        
    return hospital_data
