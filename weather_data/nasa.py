import requests
from datetime import datetime


def get_weather_data(**kwargs):
    rootURL = "https://power.larc.nasa.gov/cgi-bin/v1/DataAccess.py?" #request=execute&identifier=SinglePoint&parameters=T2M,PS,ALLSKY_SFC_SW_DWN&startDate=20160301&endDate=20160331&userCommunity=SSE&tempAverage=DAILY&outputList=JSON,ASCII&lat=36&lon=45&user=anonymous"
    params = {
        'request': 'execute',
        'identifier': 'SinglePoint', #SinglePoint, Regional, Global
        #'parameters': 'T2M,T2M_MAX,T2M_MIN,PS,PRECTOT,QV2M,RH2M,T10M,WS10M,WS2M,TS,TS_RANGE,TS_MIN,TS_MAX,ALLSKY_SFC_LW_DWN', # More than 100
        'parameters': 'T2M,T2M_MAX,T2M_MIN,PRECTOT,WS2M,RH2M,T2MDEW,ALLSKY_SFC_LW_DWN,ALLSKY_SFC_SW_DWN,ALLSKY_TOA_SW_DWN',
        'startDate': '20190101', 
        'endDate': '20190102',
        'userCommunity': 'AG', # SSE, SB, AG
        'tempAverage': 'DAILY', # DAILY, INTERANNUAL, CLIMATOLOGY
        'outputList': 'JSON', #JSON, ASCII, CSV, ICASA, NETCDF
        'lat': '36',
        'lon': '45',
        'user': 'anonymous'
    }
    #print(kwargs)
    for k in params.keys():
        if k in kwargs:
            params[k] = str(kwargs[k])

    if params['tempAverage'] == 'CLIMATOLOGY':
        params.pop('startDate')
        params.pop('endDate')
           
    paramURL = '&'.join(['{}={}'.format(k, v) for k, v in params.items()])
    URL = rootURL + paramURL
    #print(URL)
    r    = requests.get(url=URL)
    try:
        data = r.json()['features'][0]['properties']['parameter']
    except KeyError:
        #pprint.pprint(r.json())
        return 0
    data_dict = {k: list(v.values()) for k, v in data.items()}
    if params['tempAverage'] == 'DAILY':
        data_dict['date'] = [str(datetime.strptime(x, '%Y%m%d')) for x in data[list(data.keys())[0]].keys()]
    else:
        data_dict['date'] = [x for x in data[list(data.keys())[0]].keys()]

    return data_dict
