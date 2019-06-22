import responder
import os
import json
from loguru import logger

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
        rv = json.load(f)
    resp.media = rv



if __name__ == '__main__':
    api.run(address="0.0.0.0")
