from uboto3 import UBoto3
from pymongo import MongoClient
import os
import json
import pprint


if __name__ == "__main__":

    uri = "mongodb://{}:{}@{}".format(
        os.getenv("ME_CONFIG_MONGODB_ADMINUSERNAME"),
        os.getenv("ME_CONFIG_MONGODB_ADMINPASSWORD"),
        os.getenv("MONGODB_URL"))

    mongo = MongoClient(uri)
    db = mongo.velometria
    collection = db.events

    s3 = UBoto3()

    keys = s3.list_keys(Prefix='events')

    pprint.pprint(s3.get_object(keys[0]))

    for k in keys:
        pprint.pprint(k)
        obj = s3.get_object(k)
        if not collection.find_one({'slug': obj['slug']}):
            collection.insert_one(obj)
            pprint.pprint("added {}".format(k))
        else:
            pprint.pprint("key {} already exist".format(k))
