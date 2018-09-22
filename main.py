from flask import Flask, jsonify, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from pymongo import MongoClient
import os
import json


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

# Create Flask app
app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

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

@app.route('/submit', methods=('GET', 'POST'))
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('submit.html', form=form)

@app.route('/events')
def test():

    db = mongo.velometria
    docs = db.events.find()
    rv = []
    for d in docs:
        d.pop('_id')
        rv.append(d)
    return jsonify(rv)


if __name__ == "__main__":

    app.run(debug=True, host=None)
