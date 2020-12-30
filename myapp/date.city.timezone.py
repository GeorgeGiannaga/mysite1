import datetime
import timezonefinder, pytz
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="app")
import numpy as np

a = input("Write the city you want to know what time is now: ")

def geoloc(city= None):
    if city != None:
        try:
            loc = geolocator.geocode(str(city))
            b = str(loc.address).split(", ")
            return (loc.latitude, loc.longitude, b[0])
        except:
            return np.nan

c = geoloc(a)
tf = timezonefinder.TimezoneFinder()
tz_str = tf.certain_timezone_at(lat=c[0], lng=c[1])
if tz_str is None:
    print("Could not determine the time zone")
else:
    timezone = pytz.timezone(tz_str)
    dt = datetime.datetime.utcnow()
    print ("The time in %s is %s" % (c[2], dt + timezone.utcoffset(dt)))
