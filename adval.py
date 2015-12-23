"""
Address Validation Script
"""
import geopy
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
def validate_pincode(pincode):
	#add pincode validation from mysql db
	return True
def check_address(pincode, address, country):
	if not validate_pincode():
		return False
	geolocator = Nominatim()
	location = geolocator.geocode(address + ',' + country)
	if not location:
		return False
	location1 = geolocator.geocode(pincode + ',' + country)
	if not location:
		return False
	location_coordinates = (location.latitude, location.longitude)
	location1_coordinates = (location1.latitude, location1.longitude)
	if vincenty(location_coordinates, location1_coordinates).miles > 1.5:
		return False
	else:
		return True