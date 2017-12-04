from pymongo import MongoClient

client = MongoClient('mongodb://sofafafa:sofafafa1@ds141098.mlab.com:41098/ubre')
db = client['ubre']
drivers = db['drivers_test']
passengers = db['passengers_test']
trips = db['available_trips_test']
