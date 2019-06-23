from pytest import approx
import pytest
import os
import pandas as pd
from predict import ftppk_time_model, linear_predict, nwpk_time_model


@pytest.fixture
def results():
    path = os.path.normpath("assets/results")
    f_name = os.path.join(path, 'mdd-2017.json')
    df = pd.read_json(f_name)
    return df


def test_ftppk_time_model(results):
    rv = ftppk_time_model(results, 4)
    assert isinstance(rv, int)
    assert rv == 24810


def test_nwpk_time_model(results):
    rv = nwpk_time_model(results, 6*3600)
    assert rv == approx(2.744, 0.1)


def test_linear_predict():
    df = pd.DataFrame({
        "x": [1, 2, 3, 4, 5],
        "y": [1, 2, 3, 4, 5]
    })
    assert linear_predict(df.x, df.y, 3) == 3.0
    assert linear_predict(df.x, df.y, 10) == 10.0