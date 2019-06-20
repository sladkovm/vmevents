from uboto3 import UBoto3
from pymongo import MongoClient
import click
import os
import json
import pprint


@click.command()
def create_db():

    uri = "mongodb://{}:{}@{}".format(
        os.getenv("ME_CONFIG_MONGODB_ADMINUSERNAME"),
        os.getenv("ME_CONFIG_MONGODB_ADMINPASSWORD"),
        os.getenv("MONGODB_URL"))

    mongo = MongoClient(uri)
    db = mongo.velometria
    collection = db.events

    s3 = UBoto3()

    keys = s3.list_keys(Prefix='events')

    for k in keys:
        obj = s3.get_object(k)
        if not collection.find_one({'slug': obj['slug']}):
            collection.insert_one(obj)
            click.echo("added {}".format(k))
        else:
            click.echo("key {} already exist".format(k))


if __name__ == '__main__':

    create_db()
