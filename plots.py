import seaborn as sns
from matplotlib import pyplot as plt
from numpy.random import choice

from models import TimeSeries

sns.set(rc={'figure.figsize': (25, 10)})


def get_prices_plots(time_series: TimeSeries, n: int = 6):
    fig, ax = plt.subplots(ncols=3, nrows=n // 3)
    values = list(time_series.values())
    for i, pos in enumerate(choice(len(time_series), n, replace=False)):
        prices = [it.price for it in values[pos]]
        times = [it.timestamp for it in values[pos]]
        sns.lineplot(x=times, y=prices, ax=ax[i // 3, i % 3])
    return ax


def get_lengths_plot(time_series: TimeSeries):
    lengths = [len(it) for it in time_series.values()]
    return sns.countplot(x=lengths)

