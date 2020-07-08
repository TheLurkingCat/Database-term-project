def Query_type1(type,date1,date2,place):
    Table = ''
    if(type == 1):
        Table = 'City'
    elif (type == 2):
        Table = 'Country'
    elif (type == 3):
        Table = 'MajorCity'
    else:
        Table = 'State'
    SQL = 'SELECT T.dt,SUBSTR(T.AverageTemperature,1,6) From LandTemperaturesBy' + Table +  ' as T WHERE T.dt between ? and ? and T.' + Table + ' = ?'
    c.execute(SQL,(date1,date2,place))
    for row in c:
        print(row)
    return SQL  