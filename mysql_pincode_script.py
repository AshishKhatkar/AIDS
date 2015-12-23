import csv
from sets import Set
import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost", "root", "password", "Snapdeal_Hackathon")

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Drop table if it already exist using execute() method.
cursor.execute("DROP TABLE IF EXISTS PINCODES")

sql = """CREATE TABLE PINCODES (pincode CHAR(6) NOT NULL, state CHAR(50))"""
cursor.execute(sql)

distinct_pincode = Set([])

with open('all_india_pin_code.csv', 'rb') as f:

	reader = csv.reader(f)
	for row in reader:
		# print row
		distinct_pincode.add(row[1])
		

for pincode in distinct_pincode :
 	# print pincode
 	sql = "INSERT INTO PINCODES(pincode, state) VALUES ('%s', '%s')" % (row[1], row[9])
	try:
	   # Execute the SQL command
	   cursor.execute(sql)
	   # Commit your changes in the database
	   db.commit()
	except:
	   # Rollback in case there is any error
	   db.rollback()


sql = """SELECT * FROM PINCODES;"""

cursor.execute(sql)
data = cursor.fetchall()

# print(data)

db.close()

# print "Number of Distinct Pincodes : " + str(len(distinct_pincode))