from geopy.geocoders import Nominatim

def getLocation(lat, lon):
    try:
        location = geolocator.reverse(str(lat) + ',' + str(lon))
    except:
        # print('location not found')
        return 'not found'
    address = location.raw['address']
    return address


# Initialize Nominatim API 
geolocator = Nominatim(user_agent="my_geopy_app")
# Test a location
# location = getLocation(52.108352,0.924454)
location = getLocation(52.038993,0.726545)
print(location)
exit()
