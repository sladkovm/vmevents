import responder
from loguru import logger

api = responder.API()

@api.route("/hallo")
def greet_world(req, resp):
    logger.debug('vmevents')
    resp.text = "event api"


if __name__ == '__main__':
    api.run(address="0.0.0.0")
