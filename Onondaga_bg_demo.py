# -*- coding: utf-8 -*-
"""
Created on Tue May  4 13:28:42 2021

@author: Aethe
"""


# Andrew Etheridge
# Advanced Policy Analysis
# Final Assignment - Onondaga Demographic Data (Census API)
# 4/1/2021

#%%

# Imports

import pandas as pd
import requests
import geopandas as gpd

#%%

# Setting the api

api = 'https://api.census.gov/data/2018/acs/acs5'

#%%

get_what = 'B01003_001E,B02001_002E'

#%%

# Indicating to return the county and and the subset of possible records

for_clause = 'block group:*'

#%%

# Indicating to use countied only in state 36 - NY

in_clause = 'state:36 county:067'

#%%

# Entering my api key

key_value = 'fc0110b11c52d6cb376d2ac0bd1762030374fd7a'

#%%

payload = {
    'get':get_what,
    'for':for_clause,
    'in':in_clause,
    'key':key_value
    }

#%%

# Building an https query string, sending it to API, and getting response

response = requests.get(api, payload)

#%%

# Testing for correct response
## 'assert False' will stop the script if an incorrect response is received

if response.status_code == 200:
    print("\nThe request has succeeded!\n")
else:
    print(response.status_code)
    print(response.text)
    assert False

#%%

response.json()

#%%

# Parsing the JSON returned into a list of rows 

row_list = response.json()

#%%

# Setting variables to the rows

colnames = row_list[0]

datarows = row_list[1:]

#%%

# Converting to a pandas dataframe

onondaga_demo = pd.DataFrame(columns=colnames, data=datarows)

#%%

# Setting a dictionary to rename the columns in pop dataframe

new_names = {
    "B01003_001E":"pop",
    "B02001_002E":"white"
    }

#%%

# USing the dict to rename columns in pop

onondaga_demo = onondaga_demo.rename(new_names, axis='columns')

#%%

# Setting the index to GEOID

onondaga_demo['GEOID'] = onondaga_demo['state']+onondaga_demo['county']+onondaga_demo['tract']+onondaga_demo['block group']

onondaga_demo = onondaga_demo.set_index('GEOID')

#%%

# Dropping the state, county, tract, and block group columns

onondaga_demo = onondaga_demo.drop(['state', 'county','tract', 'block group'], axis='columns')


#%%

# Setting demographic columns to int

onondaga_demo = onondaga_demo.astype({"pop":int, "white":int})


#%%

# New columns:
## Number of non-white residents in the individual bg

onondaga_demo['poc'] = onondaga_demo['pop'] - onondaga_demo['white']

## Proportion of bg pop made up of poc

onondaga_demo['poc_proportion'] = onondaga_demo['poc']/onondaga_demo['pop']


#%%

# Saving as a csv

onondaga_demo.to_csv("onondaga_bg_demo.csv")

#%%

# Loading in the block group file

demo_bg = gpd.read_file("zip://tl_2018_36_bg.zip")

#%%

# Filtering to Onondaga County
demo_bg = demo_bg.query("COUNTYFP == '067'")

## Matching the projection

demo_bg = demo_bg.to_crs(epsg=26918)

## Setting the index to GEOID

demo_bg = demo_bg.set_index("GEOID")

#%%

# Merging the block group and onondaga_econ dfs

demo_bg = demo_bg.join(onondaga_demo, how="outer")

## Saving to geopackage

demo_bg.to_file("near_parcels_remed.gpkg", layer="demo_bg")

#%%