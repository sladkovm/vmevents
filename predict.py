import numpy as np
from sklearn.linear_model import LinearRegression
from loguru import logger


def remove_outliers(df):
    ftppk = df.athlete_ftp / df.athlete_weight

    mean = df.elapsed_time.mean()
    std = df.elapsed_time.std()

    return df[(df.elapsed_time < (mean + 3 * std)) & (df.elapsed_time > (mean - 3 * std)) & (ftppk > 0)].copy()


def linear_predict(x, y, x_pred):
    """Performs linear y = a*x + b fit and returns y_pred
    
    Arguments:
        x {pd.Series} -- [description]
        y {pd.Series} -- [description]
        x_pred {number} -- [description]
    
    Returns:
        number -- [description]
    """

    x = x.values
    y = y.values

    X = x[:, np.newaxis]

    model = LinearRegression().fit(X, y)
    logger.debug(model.coef_)

    x_test = np.array([x_pred]).astype(np.float64).reshape(1, -1)
    logger.debug(x_test)
    _ = model.predict(x_test)
    
    y_pred = _[0]

    return y_pred


def ftppk_time_model(df, ftppk):
    """Returns predicted time as function of ftppk"""

    X = df.athlete_ftp / df.athlete_weight
    y = df.elapsed_time

    rv = linear_predict(X, y, ftppk)

    return int(rv)



def nwpk_time_model(df, time):
    """Returns predicted nwpk as function of ftppk"""

    X = df.elapsed_time
    y = df.weighted_power / df.athlete_weight

    rv = linear_predict(X, y, time)

    return rv