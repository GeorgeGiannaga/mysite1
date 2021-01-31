from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent="app")

def geoloc(address= None, city=None):
    if address != None and city!= None:
        try:
            loc = geolocator.geocode(address, city)
            return loc.latitude, loc.longitude
        except:
            return None

print(geoloc('Pontou 5','Athens')[0])

