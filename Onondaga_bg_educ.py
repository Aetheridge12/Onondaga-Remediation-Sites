# -*- coding: utf-8 -*-
"""
Created on Tue May  4 16:41:47 2021

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

get_what = 'B15003_001E,B15003_017E,B15003_018E,B15003_019E,B15003_020E,B15003_021E,B15003_022E,B15003_023E,B15003_024E,B15003_025E'

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

onondaga_edu = pd.DataFrame(columns=colnames, data=datarows)

#%%

# Setting a dictionary to rename the columns in pop dataframe

new_names = {
    "B15003_001E":"pop_25",
    "B15003_017E":"hs",
    "B15003_018E":"ged",
    "B15003_019E":"less_1_col",
    "B15003_020E":"more_1_col",
    "B15003_021E":"associates",
    "B15003_022E":"bachelors",
    "B15003_023E":"masters",
    "B15003_024E":"professional",
    "B15003_025E":"doctorate"
    }

#%%

# USing the dict to rename columns in pop

onondaga_edu = onondaga_edu.rename(new_names, axis='columns')

#%%

# Setting the index to tract and dropping the state and county as they
# are the same throughout

# Setting the index to GEOID

onondaga_edu['GEOID'] = onondaga_edu['state']+onondaga_edu['county']+onondaga_edu['tract']+onondaga_edu['block group']

onondaga_edu = onondaga_edu.set_index('GEOID')

onondaga_edu = onondaga_edu.drop(['state','county','tract','block group'], axis='columns')


#%%

# Setting educational attainment columns to int

onondaga_edu = onondaga_edu.astype({"pop_25":int,"hs":int,"ged":int,"less_1_col":int,"more_1_col":int,"associates":int,"bachelors":int,"masters":int,"professional":int,"doctorate":int})


#%%

# Altering the columns
## Creating more broad categories
onondaga_edu['below_hs'] = onondaga_edu['pop_25'] - (onondaga_edu['hs']+onondaga_edu['ged']+onondaga_edu['less_1_col']+onondaga_edu['more_1_col']+onondaga_edu['associates']+onondaga_edu['bachelors']+onondaga_edu['masters']+onondaga_edu['professional']+onondaga_edu['doctorate'])
onondaga_edu['hs_or_ged'] = onondaga_edu['hs'] + onondaga_edu['ged']
onondaga_edu['some_college'] = onondaga_edu['associates'] + onondaga_edu['less_1_col'] + onondaga_edu['more_1_col']  
onondaga_edu['advanced_deg'] = onondaga_edu['masters'] + onondaga_edu['professional'] + onondaga_edu['doctorate']
onondaga_edu['no_college'] = onondaga_edu['below_hs']+onondaga_edu['hs_or_ged']
onondaga_edu['college'] = onondaga_edu['some_college']+onondaga_edu['bachelors']+onondaga_edu['advanced_deg']
onondaga_edu['no_college_prop'] = onondaga_edu['no_college'] / onondaga_edu['pop_25']

## Dropping unneeded columns

onondaga_edu = onondaga_edu.drop(['hs','ged','less_1_col','more_1_col','associates','masters','professional','doctorate'], axis='columns')

#%%

# Saving to csv

onondaga_edu.to_csv("onondaga_bg_educ.csv")

#%%

# Loading in the block group file

educ_bg = gpd.read_file("zip://tl_2018_36_bg.zip")

#%%

# Filtering to Onondaga County
educ_bg = educ_bg.query("COUNTYFP == '067'")

## Matching the projection

educ_bg = educ_bg.to_crs(epsg=26918)

## Setting the index to GEOID

educ_bg = educ_bg.set_index("GEOID")

#%%

# Merging the block group and onondaga_econ dfs

educ_bg = educ_bg.join(onondaga_edu, how="outer")

## Saving to geopackage

educ_bg.to_file("near_parcels_remed.gpkg", layer="educ_bg")

#%%