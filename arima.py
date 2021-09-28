import warnings
from typing import List, Tuple, Dict

import numpy
from scipy.spatial.distance import cosine
from statsmodels.tsa.arima.model import ARIMA
from tqdm.auto import tqdm

from models import Event

Order = Tuple[int, int, int]


def grid_search_arima(time_series: Dict[int, Tuple[List[Event]]], low: int, high: int) -> Order:
    pbar = tqdm(total=(high - low) ** 3, desc="ARIMA grid search")
    min_mean = None
    best_order = None
    for p in range(low, high):
        for d in range(low, high):
            for q in range(low, high):
                try:
                    metrics = [evaluate_with_arima(it[0], it[1], (p, d, q)) for it in time_series.values()]
                    mean = numpy.mean(metrics)
                    if min_mean is None or mean < min_mean:
                        min_mean = mean
                        best_order = (p, d, q)
                except:
                    pass
                finally:
                    pbar.update(1)
    pbar.close()
    return best_order


def evaluate_with_arima(train: List[Event], test: List[Event], order: Order) -> float:
    pred = predict_with_arima(train, len(test), order)
    target = [it.price for it in test]
    return cosine(pred, target)


def predict_with_arima(train: List[Event], steps: int, order: Order) -> List[float]:
    prices = [it.price for it in train]
    model = ARIMA(prices, order=order)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        fitted = model.fit()
    predictions = fitted.forecast(steps)
    return predictions
