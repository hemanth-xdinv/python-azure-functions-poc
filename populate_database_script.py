from pymongo import MongoClient
import urllib
import os
import json
import random

username = urllib.parse.quote_plus(os.environ.get("MONGO_USERNAME"))
password = urllib.parse.quote_plus(os.environ.get("MONGO_PASSWORD"))

url = f'mongodb+srv://{username}:{password}@cluster0-practice.tmxrp.azure.mongodb.net/practice-database?retryWrites=true&w=majority'

cluster = MongoClient(url)

db = cluster["practice-database"]
student = db["student"]

# Populating the database with 150 hypothetical student details

def populate_database(collection):
    names = json.loads(open("names.json", "r").read())

    for i,name in enumerate(names):
        post = {
            "_id": i,
            "first_name": name,
            "roll_num": i+1,
            "email": ''.join([name,"@school.com"]).lower(),
            "class": random.choice([i for i in range(7, 13)]),
            "section": random.choice(["A", "B"])
        }
        collection.insert_one(post)