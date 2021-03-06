from geopy.geocoders import Nominatim


geolocator = Nominatim(user_agent="app")

def geoloc(address,postalcode, country):
        x ={"address": address,
             'postalcode':postalcode,
            'country': country}
        try:
            loc = geolocator.geocode(x)
            return (loc.latitude, loc.longitude)
        except:
            return None
