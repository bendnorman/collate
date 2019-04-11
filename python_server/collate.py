# Helper functions
from census import Census
import numpy as np
import pandas as pd
import geopandas as gpd
import cenpy as cen

from us import states
from shapely.geometry import Point, Polygon
from geopy.geocoders import Nominatim

import matplotlib
matplotlib.use('PS')
import matplotlib.pyplot as plt

def address_to_loc(addr):
    """Long and Lat of (addr)"""
    zillow_shape_file = file_init()
    geolocator = Nominatim(user_agent="collate")
    location = geolocator.geocode(addr)
    location = Point(location.longitude, location.latitude)
    return {'long': location.coords[0][1], 'lat': location.coords[0][0]}





##########################

# Create shape file
def file_init(neighborhood='New York'):
    zillow_data = pd.read_csv('data/Neighborhood_Zhvi_AllHomes.csv')
    zillow_data = zillow_data[zillow_data['City'] == neighborhood]
    zillow_shape_file = gpd.read_file('data/ZillowNeighborhoods-NY/ZillowNeighborhoods-NY.shp')
    zillow_shape_file = zillow_shape_file[zillow_shape_file['City'] == neighborhood]

    return zillow_data, zillow_shape_file


# Functions for getting zillow real estate trends of an area
def address_to_neighborhood(addr):
    """Returns a Zillow neighborhood given an address"""
    zillow_shape_file = file_init()
    geolocator = Nominatim(user_agent="collate")
    location = geolocator.geocode(addr)
    location = Point(location.longitude, location.latitude)

    for i, row in zillow_shape_file.iterrows():
        polygon = row.get('geometry')
        if location.within(polygon):
            return row.get('Name')


def address_realestate_features(addr, years=2):
    # """Returns zillow data given an address"""
    neighborhood = address_to_neighborhood(addr)
    features = zillow_data[zillow_data['RegionName'] == neighborhood]
    return features.iloc[:, -12 * years:]


def plot_realestate_trends(addr, years=2):
    # """Plots zillow realestate trends given an address and year interval"""
    features = address_realestate_features(addr, years)
    x = list(features)
    addr_y = features.values.reshape(len(x))

    city_average = zillow_data[zillow_data.columns[-years * 12:]].mean(axis=0)

    plt.figure(figsize=(15, 10))
    plt.xticks(rotation=90)
    plt.plot(x, addr_y)
    plt.plot(x, city_average)
