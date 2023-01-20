import math
import pandas as pd
from shapely.geometry import Point
from shapely.ops import nearest_points


def convert_to_point(row, label_lat, label_lon):
    '''
    Returns point object from row with latitude and longitude columns. Function to use in lambda function

            Parameters:
                    row (pandas.Series): pandas row
                    label_lat (str): column name referring to latitude
                    label_lon (str): column name referring to longitude

            Returns:
                    point (shapely.geometry.Point)
    '''

    lon = float(row[label_lat])
    lat = float(row[label_lon])
    return Point(lon, lat)


def distance_points(coord1, coord2):
    '''
    Returns the distance between two coordinates in kilometers

            Parameters:
                    coord1 (tuple): lat and lon
                    coord2 (tuple): lat and lon

            Returns:
                    km (float)
    '''

    # Coordinates in decimal degrees (e.g. 2.89078, 12.79797)
    lon1, lat1 = coord1
    lon2, lat2 = coord2
    R = 6371000  # radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c  # output distance in meters
    km = meters / 1000.0  # output distance in kilometers

    meters = round(meters)
    km = round(km, 3)
    return km


def nearest_station(lat, lon, stations, label_distance="DistanceKmAgri"):
    '''
    Returns nearest station from coordinates

            Parameters:
                    lat (float): latitude value
                    lon (float): longitude value
                    stations (geopandas.GeoDataFrame): stations geodataframe
                    label_distance (str): name to assign in index

            Returns:
                    row (pandas.Series)
    '''
    
    target_point = Point(lon, lat)
    station_points = stations.geometry.unary_union
    # find the nearest point and return the corresponding Place value
    station_point = nearest_points(target_point, station_points)[1]
    mask = stations.geometry == station_point
    # print(df_ph[nearest].elevation)
    distance = distance_points([x[0] for x in station_point.coords.xy], [x[0] for x in target_point.coords.xy])

    row = stations[mask].iloc[0]
    row = row.append(pd.Series([distance], index=[label_distance]))
    
    return row
