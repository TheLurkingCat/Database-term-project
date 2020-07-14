from datetime import date
from enum import Enum
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from dateutil.relativedelta import relativedelta

from . import query


def get_data(start: date, end: date, isglobal: bool, qtype: Enum, use_month: bool, place=None) -> Tuple[List[float]]:

    if use_month:
        delta = relativedelta(months=1)
        fmt = "%Y/%m"
    else:
        fmt = "%Y"
        end.replace(month=12)
        delta = relativedelta(years=1)
    if isglobal:
        data = query.global_temperature(start, end, qtype, use_month)
    else:
        data = query.local_temperature(start, end, qtype, place, use_month)

    temp = start
    horizontal = []
    while temp <= end:
        horizontal.append(temp.strftime(fmt))
        temp += delta
    print(len(horizontal), len(data[0]), len(data[1]))
    return horizontal, data


def draw(start: date, end: date, isglobal: bool, qtype: Enum, place=None, use_bar=False, use_month=True, color='k', style='solid', subpos=111) -> None:
    figure = plt.figure("Final Project", figsize=(16, 9))
    figure.set_tight_layout({"pad": .5})
    plt.subplot(subpos)
    if use_bar:
        plot_function = plt.bar
        kwargs = {"color": color}
    else:
        plot_function = plt.errorbar
        kwargs = {"color": color, "marker": '.'}

    data = get_data(start, end, isglobal, qtype, use_month, place)
    plot_function(data[0], data[1][0], yerr=data[1][1],
                  ecolor='g', linestyle=style, **kwargs)
    plt.xticks(rotation=45)
