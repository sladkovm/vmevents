from flask import (Flask, jsonify, redirect,
                   render_template, flash, url_for)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from pymongo import MongoClient
import os
from datetime import date


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    short_name = StringField('short_name', validators=[DataRequired()])
    date = DateField(label='date',
                     format="%d-%m-%Y",
                     default=date.today(),
                     validators=[DataRequired()])
    location = StringField('location', validators=[DataRequired()])
    country = StringField('country', validators=[DataRequired()])
    distance = StringField('distance')
    elevation = StringField('elevation')
    url = StringField('url')

    submit = SubmitField('Submit')

#
# {
#     "_id": ObjectID("5ba69eecd65d781d7dcc8349"),
#     "distance": 170,
#     "results_url": [],
#     "keywords": [
#         "Espace",
#         "Espace Cycles",
#         "La Espace",
#         "Etalle"
#     ],
#     "organizer": "La Espace Cycles",
#     "edition_year": "2017",
#     "name": "Cycle Espace Etalle 2017",
#     "date": "2017-05-25",
#     "url": "http://www.espacecycles.be/la-espace-cycle/",
#     "slug": "la-espace-cycles-2017",
#     "location": "Etalle",
#     "short_name": "La Espace Cycles 2017",
#     "elevation": 2600,
#     "country": "Belgium"
# }


# Create Flask app
app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

Bootstrap(app)

# Connect to MongoDB
uri = "mongodb://{}:{}@{}".format(
    os.getenv("ME_CONFIG_MONGODB_ADMINUSERNAME"),
    os.getenv("ME_CONFIG_MONGODB_ADMINPASSWORD"),
    os.getenv("MONGODB_URL"))


mongo = MongoClient(uri)


# View the MongoDB content using Flask views
@app.route('/')
def index():
    print('index')
    return "Hello!"


@app.route('/submit/', methods=['GET', 'POST'])
def submit():
    print('submit top')
    form = MyForm()
    if form.validate_on_submit():
        flash('Post: Submitted!', 'success')

        return redirect(url_for('submit'))
    else:

        flash('Get: Not all fields are filled', 'error')
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
