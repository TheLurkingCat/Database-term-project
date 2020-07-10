def query_type1(query_type, date1, date2, place):
    table = ''
    if query_type == 1:
        table = 'City'
    elif query_type == 2:
        table = 'Country'
    elif query_type == 3:
        table = 'MajorCity'
    else:
        table = 'State'
    SQL = 'SELECT T.dt,SUBSTR(T.AverageTemperature,1,6) From LandTemperaturesBy' + \
        table + ' as T WHERE T.dt between ? and ? and T.' + table + ' = ?'
    c.execute(SQL, (date1, date2, place))
    for row in c:
        print(row)
    return SQL
