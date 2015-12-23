"""
Address Validation Script
"""
import geopy
from geopy.distance import vincenty
from geopy.geocoders import Nominatim
import MySQLdb


def validate_pincode(pincode, state):

	db = MySQLdb.connect("localhost", "root", "password", "Snapdeal_Hackathon")
	cursor = db.cursor()

	sql = "SELECT COUNT(*) FROM PINCODES WHERE pincode = '" + str(pincode) + "' AND state = '" + str(state) + "';"	
	cursor.execute(sql)
	data = cursor.fetchall()

	db.close()
	# print data
	
	if str(data) != "((0L,),)" :
		return True
	else :
		return False


def check_address(pincode, address, state, country):
	if not validate_pincode(pincode, state):
		return False
	geolocator = Nominatim()

	location = geolocator.geocode(address + ',' + state + ',' + country)
	print location
	if not location:
		return False

	location1 = geolocator.geocode(pincode + ',' + state + ',' + country)
	if not location:
		return False
	location_coordinates = (location.latitude, location.longitude)
	location1_coordinates = (location1.latitude, location1.longitude)
	if vincenty(location_coordinates, location1_coordinates).miles > 2:
		return False
	else:
		return True

