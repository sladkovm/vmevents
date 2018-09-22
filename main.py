from flask import Flask, jsonify
from pymongo import MongoClient
import os
import json

# Create Flask app
app = Flask(__name__)

# Connect to MongoDB
uri = "mongodb://{}:{}@{}".format(
    os.getenv("ME_CONFIG_MONGODB_ADMINUSERNAME"),
    os.getenv("ME_CONFIG_MONGODB_ADMINPASSWORD"),
    os.getenv("MONGODB_URL"))


mongo = MongoClient(uri)


# View the MongoDB content using Flask views
@app.route('/')
def index():
    return "Hello!"


@app.route('/test')
def test():

    doc = mongo.test_database.test_collections.find_one()
    doc.pop("_id")
    return jsonify(doc)

if __name__ == "__main__":

    app.run(debug=True, host=None)
