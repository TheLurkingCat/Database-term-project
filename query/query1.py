from datetime import date
from typing import List, Tuple
from sqlalchemy import MetaData, Table, create_engine
from dateutil.relativedelta import relativedelta

def judge_leap_year(year: int):
    if (year % 4) == 0:
        if (year % 100) == 0:
            if (year % 400) == 0:
                return 1   
            else:
                return 0
        else:
            return 1       
    else:
        return 0




def not_global_avg_temperature(start: date, end: date, Type: int , place: str ,use_month: bool):
    if use_month:
        fmt = "%Y-%m-01"
    else:
        fmt = "%Y-01-01"

    start_str = start.strftime(fmt)
    end_str = end.strftime(fmt)
    if Type == 1:     #City
        table = LandTemperaturesByCity
        query_avg_temp = table.select(table.c.AverageTemperature).where(table.c.dt >= start and table.c.dt <= end and table.c.City == place)
    elif Type == 2:   #State
        table = LandTemperaturesByState
        query_avg_temp = table.select(table.c.AverageTemperature).where(table.c.dt >= start and table.c.dt <= end and table.c.State == place)
    else:             #Country
        table = LandTemperaturesByCountry
        query_avg_temp = table.select(table.c.AverageTemperature).where(table.c.dt >= start and table.c.dt <= end and table.c.Country == place)


    ret = client.execute(query_avg_temp)
    if use_month == True:
        SUM = 0
        new_ret = []
        Days = [ 31 ,28 ,31 ,30 ,31 ,30 ,31 ,31 ,30 ,31 ,30 ,31 ]
        for i in range(1 , len(Data)/12):
            for j in range(1,12):
                SUM += ret[ 12*(i-1)+j ] * Days[j]
            newEX = SUM/365
            new_ret.append(newEX)
        return new_ret
    else:
        return ret

    return ret
def global_temperature(start: date, end: date, Type: int ,Temp_type: int ,use_month: bool):
    if use_month:
        fmt = "%Y-%m-01"
    else:
        fmt = "%Y-01-01"

    start_str = start.strftime(fmt)
    end_str = end.strftime(fmt)

    table = Temperatures
    if Type == 1:     #Land
        if Temp_type == 1:     #AVG
            query_temp = table.select(table.c.LandAverageTemperature).where(table.c.dt >= start and table.c.dt <= end)
        elif Temp_type == 2:   #MAX
            query_temp = table.select(table.c.LandMaxTemperature).where(table.c.dt >= start and table.c.dt <= end)
        else:                  #MIN
            query_temp = table.select(table.c.LandMinTemperature).where(table.c.dt >= start and table.c.dt <= end)
    else:             #Land+Ocean
        query_temp = table.select(table.c.LandAndOceanAverageTemperature).where(table.c.dt >= start and table.c.dt <= end)
    ret = client.execute(query_temp)
    if use_month == True:
        SUM = 0
        new_ret = []
        Days = [ 31 ,28 ,31 ,30 ,31 ,30 ,31 ,31 ,30 ,31 ,30 ,31 ]
        for i in range(1 , len(Data)/12):
            for j in range(1,12):
                SUM += ret[ 12*(i-1)+j ] * Days[j]
            newEX = SUM/365
            new_ret.append(newEX)
        return new_ret
    else:
        return ret

