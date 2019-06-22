import pytest
import json
import api as service


@pytest.fixture
def api():
    return service.api


def test_hello(api):
    r = api.requests.get("http://vmevents/hello")
    assert r.text == "hello"


def test_events(api):
    r = api.requests.get("http://vmevents/events/")
    assert r.text is not None
    events = json.loads(r.text)
    assert events is not None
    assert isinstance(events, list)


def test_events_slug(api):
    r = api.requests.get("http://vmevents/events/lbl-cyclo-2017")
    assert r.text is not None
    event = json.loads(r.text)
    assert event is not None
    assert isinstance(event, dict)


def test_results_slug(api):
    r = api.requests.get("http://vmevents/results/lbl-cyclo-2017")
    assert r.text is not None
    results = json.loads(r.text)
    assert results is not None
    assert isinstance(results, list)