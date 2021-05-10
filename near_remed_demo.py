# -*- coding: utf-8 -*-
"""
Created on Tue May  4 17:00:59 2021

@author: Aethe
"""

# Andrew Etheridge
# Advanced Policy Analysis
# Final Project - Block Group Demographics Map - Proximity to Remediation Site
# 5/3/2021

#%%

# Imports

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

#%%

# Reading in the block group demographics csv file

bg_demo_data = pd.read_csv("onondaga_bg_demo.csv")

#%%

# Setting the GEOID to string and making it the index

bg_demo_data = bg_demo_data.astype({"GEOID":str})

bg_demo_data = bg_demo_data.set_index("GEOID")

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

## Reminder - the parcel layer holds all parcels within 2000m of a 
## remediation site

near = gpd.read_file("near_parcels_remed.gpkg", layer="parcels")

#%%

# Creating new series with the 'PROP_CLASS' column of near df as a float type

prop_class = near['PROP_CLASS'].astype(float)

#%%

# .between() method will produce a true  value if the prop_class is
# between 200 and 299, and false if not

is_res = prop_class.between(200,299)

#%%

# Creating a datframe that consisting only of the parcel within the 
# 200-299 range

houses = near[is_res]

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

#%%

# Creating shares df which shows the share of houses at each radius for 
# their respective block group

shares = houses.div(count_res['count'], axis='index')

#%%

# Restacking the radii for each block group, which will be used when finding
# the demographic makeup of each block group

stacked = shares.stack()

#%%

# Creating empty df - by_race

by_race = pd.DataFrame()

#%%

# Adding a column to by_race df that holds the estimated number of 
# white residents in each radius of a block group

by_race['white'] = stacked * bg_demo_data['white']

#%%

# Repeating the above step to estimate the amount of people who id
# as a poc in each radius of a block group

by_race['poc'] = stacked * bg_demo_data['poc']

#%%

# Creating a dataframe that holds the estimated population by race for each
# radius level

by_race_ring = by_race.sum(level=1)

#%%

# Finding the probability that a random resident of each race will live
# in each zone

prob = by_race_ring / by_race_ring.sum()

#%%

# Finding the odds that a poc lives in a radius, relative to a white person.

ratio = prob['poc'] / prob['white']

#%%

#

fig, ax1 = plt.subplots(dpi=300)

fig.suptitle("Probability of Radius Level, by Race")

prob.plot.bar(y=['poc', 'white'], ax=ax1)

## Setting x-axis label

ax1.set_xlabel("Distance from Remediation Site")

## Setting y-axis label

ax1.set_ylabel("Probability") 

## Tightening the layout and saving

fig.tight_layout()
fig.savefig("prob_by_race_remed.png")

#%%


# Creating the second graph

fig, ax1 = plt.subplots(dpi=300)

## Setting the title

fig.suptitle("Odds Ratio of Location, POC to White")

## Bar plot

ratio.plot.bar(ax=ax1)

## Setting x-axis label

ax1.set_xlabel("Distance from Remediation Site")

## Setting y-axis label

ax1.set_ylabel("Ratio")

## Tightening the layout and saving

fig.tight_layout()
fig.savefig("odds_ratio_remed.png")


#%%