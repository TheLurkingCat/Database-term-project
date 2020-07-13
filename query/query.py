from datetime import date
from enum import Enum
from typing import List, Tuple

import numpy as np
from dateutil.relativedelta import relativedelta
from sqlalchemy import MetaData, Table, and_, create_engine

engine = create_engine(
    'sqlite:///project.db?check_same_thread=False')
metadata = MetaData(engine)
client = engine.connect()

LandTemperaturesByCity = Table(
    'LandTemperaturesByCity', metadata, autoload=True)
LandTemperaturesByState = Table(
    'LandTemperaturesByState', metadata, autoload=True)
LandTemperaturesByCountry = Table(
    'LandTemperaturesByCountry', metadata, autoload=True)
Temperatures = Table('Temperatures', metadata, autoload=True)


class TableType(Enum):
    CITY = 1
    STATE = 2
    COUNTRY = 3


class TempType(Enum):
    LANDAVG = 1
    LANDMAX = 2
    LANDMIN = 3
    BOTHAVG = 4


def local_temperature(start: date, end: date, table_type: TableType, place: str, use_month: bool):
    if use_month:
        start_fmt = "%Y-%m-01"
        end_fmt = "%Y-%m-01"
    else:
        start_fmt = "%Y-01-01"
        end_fmt = "%Y-12-31"

    start_str = start.strftime(start_fmt)
    end_str = end.strftime(end_fmt)
    if table_type == TableType.CITY:
        table = LandTemperaturesByCity
        query = table.select().with_only_columns(
            [table.c.AverageTemperature, table.c.AverageTemperatureUncertainty]
        ).where(
            and_(
                (table.c.dt >= start),
                (table.c.dt <= end),
                (table.c.City == place)
            )
        )
    elif table_type == TableType.STATE:  # State
        table = LandTemperaturesByState
        query = table.select().with_only_columns(
            [table.c.AverageTemperature, table.c.AverageTemperatureUncertainty]
        ).where(
            and_(
                (table.c.State == place),
                (table.c.dt >= start_str),
                (table.c.dt <= end_str)
            )
        )
    elif table_type == TableType.COUNTRY:
        table = LandTemperaturesByCountry
        query = table.select().with_only_columns(
            [table.c.AverageTemperature, table.c.AverageTemperatureUncertainty]
        ).where(
            and_(
                (table.c.dt >= start_str),
                (table.c.dt <= end_str),
                (table.c.Country == place)
            )
        )
    else:
        raise ValueError("Unknown table")
    query = query.order_by(table.c.dt.asc())
    ret = np.array(list(client.execute(query)))
    if use_month:
        return ret
    return np.array([x.transpose().mean(axis=1) for x in ret.reshape(-1, 12, 2)])


def global_temperature(start: date, end: date, temp_type: TempType, use_month: bool):
    if use_month:
        start_fmt = "%Y-%m-01"
        end_fmt = "%Y-%m-01"
    else:
        start_fmt = "%Y-01-01"
        end_fmt = "%Y-12-31"

    start_str = start.strftime(start_fmt)
    end_str = end.strftime(end_fmt)

    table = Temperatures

    if temp_type == TempType.LANDAVG:
        query = table.select().with_only_columns(
            [
                table.c.LandAverageTemperature,
                table.c.LandAverageTemperatureUncertainty
            ]
        )
    elif temp_type == TempType.LANDMAX:
        query = table.select().with_only_columns(
            [
                table.c.LandMaxTemperature,
                table.c.LandMaxTemperatureUncertainty
            ]
        )
    elif temp_type == TempType.LANDMIN:  # MIN
        query = table.select().with_only_columns(
            [
                table.c.LandMinTemperature,
                table.c.LandMinTemperatureUncertainty
            ]
        )
    elif temp_type == TempType.BOTHAVG:  # Land+Ocean
        query = table.select().with_only_columns(
            [
                table.c.LandAndOceanAverageTemperature,
                table.c.LandAndOceanAverageTemperatureUncertainty
            ]
        )
    else:
        raise ValueError("Unknown temperature type")

    query = query.where(
        and_(
            (table.c.dt >= start_str),
            (table.c.dt <= end_str)
        )
    ).order_by(
        table.c.dt.asc()
    )

    ret = np.array(list(client.execute(query)))
    if use_month:
        return ret
    return np.array([x.transpose().mean(axis=1) for x in ret.reshape(-1, 12, 2)])


if __name__ == '__main__':
    start = date(1917, 1, 1)
    end = date(1920, 1, 1)
    Type = TableType.STATE
    temp = TempType.BOTHAVG
    place = 'Alagoas'
    a = global_temperature(start, end, temp, False)
    for year_avg in a:
        print(year_avg)
