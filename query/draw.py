from datetime import date

import matplotlib.pyplot as plt
import numpy as np
from dateutil.relativedelta import relativedelta


def get_data(start: date, end: date, use_month: bool) -> tuple:
    if use_month:
        delta = relativedelta(months=1)
        fmt = "%Y/%m"
    else:
        fmt = "%Y"
        delta = relativedelta(years=1)
    horizontal = []
    while start < end:
        horizontal.append(start.strftime(fmt))
        start += delta
    return horizontal, np.random.randn(len(horizontal))


def draw(start: date, end: date, use_bar=False, use_month=True):
    if use_bar:
        plot_function = plt.bar
        kwargs = {"color": 'k'}
    else:
        plot_function = plt.plot
        kwargs = {"color": 'k', "marker": '.'}

    data = get_data(start, end, use_month)
    plt.subplot(2, 1, 1)
    plot_function(*data, **kwargs)
    plt.xticks(rotation=45)
    plt.subplot(2, 2, 3)
    kwargs['color'] = 'r'
    plot_function(*data, **kwargs)
    plt.xticks(rotation=45)
    plt.subplot(2, 2, 4)
    kwargs['color'] = 'b'
    plot_function(*data, **kwargs)
    plt.xticks(rotation=45)
    plt.show()

def main():
    start = date(1975, 1, 1)
    end = date(2020, 12, 31)
    draw(start, end, False, False)

if __name__ == '__main__':
    figure = plt.figure(figsize=(16, 9))
    figure.set_tight_layout({"pad": .5})
    main()