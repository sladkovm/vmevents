import pymongo
from pymongo import MongoClient
import os
import pprint

uri = "mongodb://{}:{}@{}".format(
    os.getenv("ME_CONFIG_MONGODB_ADMINUSERNAME"),
    os.getenv("ME_CONFIG_MONGODB_ADMINPASSWORD"),
    os.getenv("MONGODB_URL"))

client = MongoClient(uri)


if client.address:
    print(client.database_names())
else:
    print("Can not connect to MongoDB")

"""
An important note about collections (and databases) in MongoDB is
that they are created lazily - none of the above commands
have actually performed any operations on the MongoDB server.

Collections and databases are created when the first document is inserted into them.
"""

db = client.test_database
print(db)

collection = db.test_collections
print(collection)

test_item = {"name": "Maksym",
             "sex": "male"}

item_id = collection.insert_one(test_item).inserted_id
print(item_id)


pprint.pprint(collection.find_one({"name": "Maksym"}))
