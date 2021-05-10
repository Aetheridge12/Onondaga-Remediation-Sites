# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 16:54:04 2021

@author: Aethe
"""

# Andrew Etheridge
# Advanced Policy Analysis
# Final Project - Remediation Site Buffers
# 4/29/2021

#%%

# Imports

import geopandas as gpd

#%%

# Reading the Remediation Site Border file

ny_remediation = gpd.read_file("Remediation_site_borders.shp")

# Reading the NY County Tracts

block_group = gpd.read_file("zip://tl_2018_36_bg.zip")

#%%

# Filtering to block groups in Onondaga County

on_bg = block_group.query("COUNTYFP == '067'")

#%%

# Creating projected layers of the block gorups and the 
# remediation site boundaries

## Projecting the tracts

pro_bg= on_bg.to_crs(epsg=6347)

## Projecting the remediation site boundaries

pro_remediation = ny_remediation.to_crs(epsg=6347)

pro_remediation = pro_remediation.query("COUNTY == 'Onondaga'")

#%%

# Dissolving the polygons in the projected remediation layer

dis_remediation = pro_remediation.dissolve(by="COUNTY", aggfunc="first")

#%%

# Creating a buffer around the remediation sites (1km)

buffer = dis_remediation.buffer(1000)

#%%

# Sending layers to onondaga.gpkg file

pro_bg.to_file("onondaga_remediation.gpkg", layer='block_group', driver='GPKG')

pro_remediation.to_file("onondaga_remediation.gpkg", layer='remediation', driver='GPKG')

buffer.to_file("onondaga_remediation.gpkg", layer='buffer', driver='GPKG')

#%%