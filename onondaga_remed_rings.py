# -*- coding: utf-8 -*-
"""
Created on Tue May  4 17:21:10 2021

@author: Aethe
"""

# Andrew Etheridge
# Advanced Policy Analysis
# Final Project - Remediation Site Rings
# 5/4/2021

#%%

# Imports

import pandas as pd
import geopandas as gpd

#%%

# Reading the Remediation Site Border file

ny_remediation = gpd.read_file("onondaga_remediation.gpkg", layer="remediation")

# Reading the NY County Tracts

block_groups = gpd.read_file("zip://tl_2018_36_bg.zip")

#%%

# Dissolving the remediation layer

dissolve = ny_remediation.dissolve(by="COUNTY", aggfunc="first")

#%%

# Mathing the projection to what is used for Onondaga County

dissolve = dissolve.to_crs(epsg=26918)

#%%

# Creating a list of integers that will be used for our rings later on

radius = [200,400,600,800,1000,2000]

#%%

# Creating an empty geodataframe

ring_layer = gpd.GeoDataFrame()

#%%

# Adding a column, "radius", that is equal to the radius variable set earlier

ring_layer['radius'] = radius

#%%

# Creating an empty list to hold the geometries of the rings

geo_list = []

#%%

# Creating a variable that is equal to None, which will be used in the 
# for loop coming next

last_buf = None

#%%

# ???

for r in radius:
    this_buf = dissolve.buffer(r)
    if len(geo_list) == 0:
        geo_list.append(this_buf[0])
    else:
        change = this_buf.difference(last_buf)
        geo_list.append(change[0])
    last_buf = this_buf

#%%

# Creating a new column 'geometry' to ring_layer which contains geo_list
## This loads the polygons for each ring into the layer

ring_layer['geometry'] = geo_list

#%%

# Mathcing the projection to what is used for Onondaga County

ring_layer = ring_layer.set_crs(epsg=26918)

#%%

# Saving ring_layer to a geopackage

ring_layer.to_file("onondaga_remed_rings.gpkg", layer="rings")

#%%

# Reading in the Onondaga tax parcel geopackage

parcels = gpd.read_file("onondaga-tax-parcels.gpkg")


## Filter to Just Resedential
#%%

# Overlaying the ring layer on to the parcels

near = gpd.overlay(parcels,ring_layer,how="intersection")

parcels_ii = gpd.read_file("onondaga-tax-parcels.gpkg")

all_values = gpd.overlay(parcels_ii,ring_layer,how="union")

#%%

# Saving to geopackage and to csv

near.to_file("near_parcels_remed.gpkg", layer="parcels")

all_values.to_file("near_parcels_remed.gpkg", layer="far_parcels")

## Dropping geometry column

near = near.drop(['geometry'], axis='columns')

near.to_csv("near_parcels_remediation.csv", index=False)

#%%