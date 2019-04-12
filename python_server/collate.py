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


class Collate:
    def __init__(self):
        zillow = self.file_init()
        self.zillow_data = zillow[0]
        self.zillow_shape_file = zillow[1]
        # self.pluto = gpd.read_file('data/pluto_census_tract.geojson')
        self.census = Census("13c056d339e329f0a4fbef4384e3667e505a55da")
        self.pluto_to_ct = pd.read_csv('data/pluto_to_ct.csv')

    def file_init(self, city='New York'):
        """Initializes the data for Collate()"""
        zillow_data = pd.read_csv('data/Neighborhood_Zhvi_AllHomes.csv')
        zillow_data = zillow_data[zillow_data['City'] == city]

        zillow_shape_file = gpd.read_file(
            'data/ZillowNeighborhoods-NY/ZillowNeighborhoods-NY.shp')
        zillow_shape_file = zillow_shape_file[zillow_shape_file['City'] == city]

        return zillow_data, zillow_shape_file

    def address_data_request(self, addr):
        location_json = self.address_to_loc_json(addr)
        real_estate_data = self.address_realestate_features(addr)
        census_data = self.address_to_census_data(addr)

        # polygon = self.address_to_polygon(addr)

        full_json = {'location': location_json,
                     'real_estate_data': real_estate_data,
                     'census_data': census_data}

        return full_json

    def address_to_loc_json(self, addr):
        """Returns a json of Long and Lat of (addr)"""
        # TODO: will fail if addr not valid!
        geolocator = Nominatim(user_agent="collate")
        location = geolocator.geocode(addr)
        location = Point(location.longitude, location.latitude)
        return {'long': location.coords[0][1], 'lat': location.coords[0][0]}

    def address_to_loc(self, addr):
        """Long and Lat of (addr)"""
        geolocator = Nominatim(user_agent="collate")
        return Point(geolocator.geocode(addr).longitude, geolocator.geocode(addr).latitude)

    # Functions for getting zillow real estate trends of an area
    def address_to_neighborhood(self, addr):
        """Returns a Zillow neighborhood given an address"""
        location = self.address_to_loc(addr)

        for i, row in self.zillow_shape_file.iterrows():
            polygon = row.get('geometry')
            if location.within(polygon):
                return row.get('Name')

    def address_realestate_features(self, addr):
        # """Returns zillow data given an address"""

        neighborhood = self.address_to_neighborhood(addr)
        features = self.zillow_data[self.zillow_data['RegionName']
                                    == neighborhood]
        # print(features.iloc[:, 7:])
        return {'real_estate': features.iloc[:, 7:].to_json()}

    def address_to_census_data(self, addr):
        pop = pd.DataFrame(self.census.acs5.get('B01003_001E', geo={'for': 'tract:*',
                                                          'in': 'state:{}'.format(states.NY.fips)}))
        income = pd.DataFrame(self.census.acs5.get('B19013_001E', geo={'for': 'tract:*',
                                                                       'in': 'state:{}'.format(states.NY.fips)}))

        addr_tract = self.reformat_pluto_tract_num(
            self.pluto_to_ct[self.pluto_to_ct['address'] == addr]['ct2010'].values[0])

        tract_income = float(
            income[income['tract'] == addr_tract]['B19013_001E'])
        tract_population = float(
            pop[pop['tract'] == addr_tract]['B01003_001E'])

        return {"income": tract_income, "population": tract_population}

    def reformat_pluto_tract_num(self, tract):
        tract = str(tract)
        tract = tract.replace(".", "")
        while len(tract) < 6:
            tract = '0' + tract
        return tract

    def address_to_bbl(self, addr):
        return self.pluto.loc[self.pluto['address'].contains(addr, na=False)]['bbl']

    def address_to_polygon(self, addr):
        return self.pluto.loc[self.pluto['address'] == addr]['geometry']
#
#
#
#
#
# ##########################
#
# # Create shape file
# # assumption! city needs to be inputted
#
#
#

#
#
# def plot_realestate_trends(addr):
#     # """Plots zillow realestate trends given an address and year interval"""
#     zillow_data, _ = file_init()
#
#     features = address_realestate_features(addr)
#     x = list(features)
#     addr_y = features.values.reshape(len(x))
#
#     city_average = zillow_data.iloc[:, 7:].mean(axis=0)
#
#     plt.figure(figsize=(15, 10))
#     plt.xticks(rotation=90)
#     plt.plot(x, addr_y)
#     plt.plot(x, city_average)
