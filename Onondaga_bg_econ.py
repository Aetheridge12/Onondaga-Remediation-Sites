# -*- coding: utf-8 -*-
"""
Created on Tue May  4 13:33:47 2021

@author: Aethe
"""

# Andrew Etheridge
# Advanced Policy Analysis
# Final Assignment - Onondaga Economic Data (Census API)
# 4/1/2021

#%%

# Imports

import pandas as pd
import requests
import numpy as np
import geopandas as gpd

#%%

# Setting the api

api = 'https://api.census.gov/data/2018/acs/acs5'

#%%

## Population by block group, median earnings by block group

get_what = 'B01003_001E,B20002_001E'

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

onondaga_econ = pd.DataFrame(columns=colnames, data=datarows)

#%%

# Setting a dictionary to rename the columns in pop dataframe

new_names = {
    "B01003_001E":"pop",
    "B20002_001E":"earnings"
    }

#%%

# USing the dict to rename columns in pop

onondaga_econ = onondaga_econ.rename(new_names, axis='columns')

#%%

# Setting the index to GEOID

onondaga_econ['GEOID'] = onondaga_econ['state']+onondaga_econ['county']+onondaga_econ['tract']+onondaga_econ['block group']

onondaga_econ = onondaga_econ.set_index('GEOID')

#%%

# Dropping the uneeded columns

onondaga_econ = onondaga_econ.drop(['state','county', 'tract', 'block group'], axis='columns')


#%%

# Setting economic columns to int

onondaga_econ = onondaga_econ.astype({"pop":int, "earnings":int})

#%%

# Setting the witheld data to NaN
## Source for code: https://stackoverflow.com/questions/55801017/how-to-replace-outliers-with-nan-while-keeping-row-intact-using-pandas-in-python

for col in onondaga_econ.columns:
    s = onondaga_econ['earnings']
    outlier_s = s<=0
    onondaga_econ['earnings'] = s.where(~outlier_s,np.nan)

#%%

# SAving to csv

onondaga_econ.to_csv("onondaga_bg_econ.csv")

#%%

# Loading in the block group file

econ_bg = gpd.read_file("zip://tl_2018_36_bg.zip")

#%%

# Filtering to Onondaga County
econ_bg = econ_bg.query("COUNTYFP == '067'")

## Matching the projection

econ_bg = econ_bg.to_crs(epsg=26918)

## Setting the index to GEOID

econ_bg = econ_bg.set_index("GEOID")

#%%

# Merging the block group and onondaga_econ dfs

econ_bg = econ_bg.join(onondaga_econ, how="outer")

## Saving to geopackage

econ_bg.to_file("near_parcels_remed.gpkg", layer="earnings_bg")

#%%