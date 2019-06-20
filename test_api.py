import pytest
import api as service


@pytest.fixture
def api():
    return service.api


def test_hello(api):
    r = api.requests.get("http://vmevents/hello")
    assert r.text == "hello"