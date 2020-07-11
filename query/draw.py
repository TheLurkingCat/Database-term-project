from datetime import date
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from dateutil.relativedelta import relativedelta


def get_data(start: date, end: date, use_month: bool) -> List[Tuple[List[float]]]:
    if use_month:
        delta = relativedelta(months=1)
        fmt = "%Y/%m"
    else:
        fmt = "%Y"
        delta = relativedelta(years=1)

    ret = []

    for _ in range(3):
        temp = start
        horizontal = []
        while temp < end:
            horizontal.append(temp.strftime(fmt))
            temp += delta
        ret.append((horizontal, np.random.randn(len(horizontal))))
    return ret


def draw(start: date, end: date, use_bar=False, use_month=True) -> None:
    style = ('solid', 'dashed', 'dashdot', 'dotted')
    if use_bar:
        plot_function = plt.bar
        kwargs = {"color": 'k'}
    else:
        plot_function = plt.plot
        kwargs = {"color": 'k', "marker": '.'}

    plt.subplot(2, 1, 1)
    dataset = get_data(start, end, use_month)
    for idx, data in enumerate(dataset):
        plot_function(*data, linestyle=style[idx % 4], **kwargs)
    plt.xticks(rotation=45)

    plt.subplot(2, 2, 3)
    kwargs['color'] = 'r'
    dataset = get_data(start, end, use_month)
    for idx, data in enumerate(dataset):
        plot_function(*data,  linestyle=style[idx % 4], **kwargs)
    plt.xticks(rotation=45)

    plt.subplot(2, 2, 4)
    kwargs['color'] = 'b'
    dataset = get_data(start, end, use_month)
    for idx, data in enumerate(dataset):
        plot_function(*data, linestyle=style[idx % 4], **kwargs)
    plt.xticks(rotation=45)
    plt.show()


def main():
    start = date(1975, 1, 1)
    end = date(2020, 12, 31)
    draw(start, end, False, False)


if __name__ == '__main__':
    figure = plt.figure("Global temperature", figsize=(16, 9))
    figure.set_tight_layout({"pad": .5})
    main()
