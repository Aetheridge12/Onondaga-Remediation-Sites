# -*- coding: utf-8 -*-
"""
Created on Tue May  4 17:00:59 2021

@author: Aethe
"""

# Andrew Etheridge
# Advanced Policy Analysis
# Final Project - Block Group Total AV - Proximity to Remediation Site
# 5/3/2021

#%%

# Imports

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

#%%

# Reading in the csv file with # of resedential parcels in a given 
# block group, and setting GEOID to string

## Reading the file

count_res = pd.read_csv("class_200_by_bg.csv")

## Setting GEOID to string

count_res = count_res.astype({"GEOID":str})

## Setting index to GEOID

count_res = count_res.set_index('GEOID')

#%%

# Read in the near_parcels_remed.gpkg from Part 1

## Reminder - the parcel layer holds all tax parcels in Onondaga County

far = gpd.read_file("near_parcels_remed.gpkg", layer="far_parcels")

## Filling all nan values with 2999, as these tac parcels are outside
## of the 2000m ring

far = far.fillna(2999)

#%%

# Creating new series with the 'PROP_CLASS' column of near df as a float type

prop_class = far['PROP_CLASS'].astype(float)

#%%

# .between() method will produce a true  value if the prop_class is
# between 200 and 299, and false if not

is_res = prop_class.between(200,299)

#%%

# Creating a datframe that consisting only of the parcel within the 
# 200-299 range

houses = far[is_res]

#%%

# Reading in the census block group file

bg_geo= gpd.read_file("zip://tl_2018_36_bg.zip")

#%%

# Filtering down bg_geo to only include Onondaga County, matching the 
# projection to what is used by Onondaga County, and dropping all columns 
# in the df besides "GEOID" and "geometry"

## Filtering to Onondaga County

bg_geo = bg_geo.query("COUNTYFP == '067'")

## Matching the projection

bg_geo = bg_geo.to_crs(epsg=26918)

## Dropping the irrelevant columns

keep_list = ["GEOID", "geometry"]

bg_geo = bg_geo[keep_list]

#%%

# Using a spatial join to to add bg GEOID values for each house

houses_by_bg = gpd.overlay(houses,bg_geo,how="intersection")

#%%

# Creating a df consisting of the house count at in each block group
# and radius

grouped = houses_by_bg.groupby(["GEOID", "radius"]).size()

#%%

keep = ['GEOID',"TOTAL_AV","radius"]

total_av = houses_by_bg[keep]

av_grouped = total_av.groupby(['radius']).sum('TOTAL_AV')


#%%

# Unstacking by radius and filling in any block group and radius 
# combination with no houses

near_counts = grouped.unstack(fill_value=0)


#%%

# Adding column to count_res df that has the number of houses near a 
# remediation site

count_res['near'] = near_counts.sum(axis='columns')

#%%

# Replacing the null data with 0

count_res['near'] = count_res['near'].fillna(0)

#%%

# Adding a column 'far' to the df which is a count of houses not near
# a remediation site for each block group

count_res['far'] = count_res['count'] - count_res['near']

#%%

# Adding an entry for each block group in the county

houses = pd.DataFrame(index=count_res.index)

#%%

# Joining near_counts df on to houses df by their index

houses = houses.join(near_counts)

#%%

# Adding a column to houses df which contains all of the houses beyond 2000m
# from a remediation site

houses['2999'] = count_res['far']

#%%

# Filling the null values in the updated houses df with zeros

houses = houses.fillna(0)

houses = houses.sum()



#%%

# Finding the average Total Assessed Value by dividing the sum at each radius
# level by the total count of houses at each radisu level. Then cleaning up
# the dataframe

## Doing the caluclation

avg_tav = av_grouped['TOTAL_AV'] / houses

## Reseting the index

avg_tav = avg_tav.reset_index()

## Setting the column name to radius and converting to an integer type

avg_tav['radius'] = avg_tav['index'].astype(int)

## Dropping the last row

avg_tav = avg_tav.drop([7])

## Dropping the unneeded column

avg_tav = avg_tav.drop(['index'], axis='columns')

## Renaming the first column to 'TOTAL_AV'

avg_tav.columns.values[0] = 'TOTAL_AV'

## Setting the index to radius

avg_tav = avg_tav.set_index('radius')

#%%

# Plotting the Total Assessed Value at each radius level

fig, ax1 = plt.subplots(dpi=300)

## Setting the title

fig.suptitle("Average Total Assessed Value, by Radius")

## Bar plot

avg_tav.plot.bar(ax=ax1)

## Setting x-axis label

ax1.set_xlabel("Distance from Remediation Site (m)")

## Setting y-axis label

ax1.set_ylabel("Average Total Assessed Value")

## Tightening the layout and saving

fig.tight_layout()
fig.savefig("avg_tav_radius.png")

#%%