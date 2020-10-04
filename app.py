from flask import Flask
import pymongo
from pymongo import MongoClient
import time
from datetime import datetime


app = Flask(__name__)

client = MongoClient("mongodb+srv://phumidea:Fifaonline321@activity.dipif.mongodb.net/test?authSource=admin&replicaSet=atlas-11eudt-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")

db_list = client.list_database_names() 

if "docker-compose" not in db_list:
	db = client["docker-compose"]
	counter = db["counter"]
	counter.insert_one({"counter":0, "time":str(datetime.now())})
	count = 0
else:
	db = client["docker-compose"]
	counter = db["counter"]
	count = counter.find_one(sort = [("counter",-1)])["counter"]

def get_hit_count():
	retries = 5
	while True:
		try:
			count = counter.find_one(sort = [("counter",-1)])["counter"]
			result = count+1
			counter.insert_one({"counter":result, "time":str(datetime.now())})
			return result
		except pymongo.errors.ConnectionFailure as exc:
			if retries == 0:
				raise exc
			retries -= 1
			time.sleep(0.5)

@app.route('/')
def hello():
	count = get_hit_count()
	return "Hello World I have been seen {} times.\n".format(count)