import responder
import os
import json
from loguru import logger
import pandas as pd
import numpy as np
from predict import remove_outliers, ftppk_time_model, nwpk_time_model


api = responder.API()

@api.route("/hello")
def hello(req, resp):
    logger.debug('vmevents')
    resp.text = "hello"


@api.route("/events/")
def events(req, resp):
    """return all events as a json list"""
    path = os.path.normpath("assets/events")
    files = os.listdir(path)
    logger.debug(files)
    rv = []
    for f_name in files:
        with open(os.path.join(path, f_name)) as f:
            _ = json.load(f)
            rv.append(_)
    resp.media = rv


@api.route("/events/{slug}")
def event(req, resp, *, slug):
    """return an event by it's slug"""
    path = os.path.normpath("assets/events")
    f_name = os.path.join(path, f"{slug}.json")
    logger.debug(f_name)
    with open(f_name) as f:
        rv = json.load(f)
    resp.media = rv


@api.route("/results/{slug}")
def results(req, resp, *, slug):
    """return an event results by it's slug"""
    path = os.path.normpath("assets/results")
    f_name = os.path.join(path, f"{slug}.json")
    logger.debug(f_name)
    with open(f_name) as f:
        _ = json.load(f)

    df = pd.DataFrame(_)

    # Fill na with forward fill
    # TO-DO: replace with fitted value as a function of time
    df['ftppk'].fillna(method='ffill', inplace=True)
    df['athlete_ftp'].fillna(method='ffill', inplace=True)
    df['IF'] = df['weighted_power'] / df['athlete_ftp']
    df['IF'] = df['IF'].replace([np.inf, -np.inf], 0.7)

    rv = json.loads(df.to_json(orient='records',
                    date_format='epoch',
                    date_unit='s'))

    resp.media = rv


@api.route("/timepred/{slug}")
def timepred(req, resp, *, slug):
    logger.debug(slug)
    params = req.params
    logger.debug(params)
    ftppk = params.get('ftppk', None)
    if ftppk is None:
        raise ValueError("ftppk is None")
    logger.debug(ftppk)

    path = os.path.normpath("assets/results")
    f_name = os.path.join(path, f"{slug}.json")
    logger.debug(f_name)

    df = pd.read_json(f_name)

    df = remove_outliers(df)
    t = ftppk_time_model(df, ftppk)
    nwpk = nwpk_time_model(df, t)

    rv = {"time_s": t,
          "nwpk": nwpk}

    logger.debug(rv)
    resp.media = rv


if __name__ == '__main__':
    api.run(address="0.0.0.0")
