import responder
import os
import json
from loguru import logger

api = responder.API()

@api.route("/hallo")
def greet_world(req, resp):
    logger.debug('vmevents')
    resp.text = "event api"


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


if __name__ == '__main__':
    api.run(address="0.0.0.0")
