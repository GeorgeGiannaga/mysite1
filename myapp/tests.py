from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="app")

def geoloc(address= None):
    if address != None:
        try:
            loc = geolocator.geocode(str(address))
            return loc.latitude, loc.longitude
        except:
            return None

print(geoloc('Filis 233')[0])
