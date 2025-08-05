from geopy.geocoders import Nominatim
from time import sleep

geolocator = Nominatim(user_agent="madlan-app")

def geocode_address(property_obj):
    address = property_obj.full_address()

    try:
        location = geolocator.geocode(address)
        sleep(1)  # Be respectful to the service

        if location:
            property_obj.latitude = location.latitude
            property_obj.longitude = location.longitude
            print(f"✅ Geocoded: {address} → ({location.latitude}, {location.longitude})")
        else:
            print(f"⚠️ Geocoding failed for: {address}")
    except Exception as e:
        print(f"🚨 Error during geocoding {address}: {e}")