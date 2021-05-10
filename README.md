# Onondaga-Remediation-Sites
An overview of the areas surrounding remediation sites within Onondaga County, New York.

**Background**
Areas of pollution, such as Brownfield and Superfund Sites can be a detriment to environmental and human health, property value, and safety. To reverse these impacts, various levels of government undertake programs to remediate these polluted sites. By observing the characteristics of the areas surrounding the sites that have been, or are currently being remediated, one can have a better understanding who has been subjected to areas of pollution.

This project will take a closer look at the characteristics of the block groups within 2000m of remediation sites within Onondaga County, New York, comparing them to the block groups 2000m or further from these sites. The observed variables include the demographic composition, the median earnings, the educational attainment, and the average total assessed value of the parcels in a block group. From this analysis, the block groups surrounding remediation sites in Onondaga County are found to be disproportionately inhabited by people of color,  people with lower educational attainment, and possess lower total assessed  property value amounts.

Once a better understanding of who has been subjected to polluted sites is understood, one can then look at the block groups in the future to see if remediation has played an impact on the population characteristics. The concern is that by raising environmental and human health conditions, safety levels, and property values, environmental justice communities will no longer be able to afford living there, displacing them away from their homes back into areas of high pollution. By reassessing the areas surrounding these remediation sites in the future, there can be an analysis of who is actually benefitting from the remediation.

**Data Files and Folder Structure**

Understanding the composition of the block groups in Onondaga County, several scripts and a QGIS file were created. Relevant data was pulled from multiple sources:
The block group shape file for New York State was pulled from the United States Census Bureau’s TIGER/LINE Shapefiles found here: https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html. To download this data, the user will need to select the year 2018, click on the web interface link, and select the relevant year and layer type. 

In several of the scripts, data was pulled from the United States Census Bureau’s 2018 American Community Survey 5-year data estimates. This was done using an API call and can be seen in the scripts

The file containing the remediation site shape file for Onondaga County was pulled from the New York State Department of Environmental Conservation’s “Environmental Site Remediation Database” found here: https://www.dec.ny.gov/cfmx/extapps/derexternal/index.cfm?pageid=3. To download this data, select “Onondaga County” under the “Search Method 2” option, and hit submit. The file has been unzipped for the purpose of this project – use the “Remediation_site_borders.shp” file.

A trimmed version of the Onondaga Tax Parcel dataset was provided by Dr. Wilcoxen of the Maxwell School at Syracuse University, during the Advanced Policy Analysis Course. (Ask for permission)

A csv file containing the count of residential properties in each block group within Onondaga County was also provided by Dr. Wilcoxen of the Maxwell School at Syracuse University, during the Advanced Policy Analysis Course. (Ask for permission)

**The files of this repository do the following:**

•	Inputs: Holds the input files listed above, minus the Onondaga Tax Parcel dataset and the csv file containing the residential property count for each block group in Onondaga County. Please contact me to discuss possible use.

•	Outputs: Holds all maps and graphs in the form of .png files. The titles of each output will be identified when the specific parts of the project are discussed below. 

•	Csv: This folder holds three csv files that are used when looking at the differences between block groups that are within 2000m of the remediation sites and those beyond that distance.

•	qgz: This folder holds the “onondaga_remed.qgz” file used to produce the maps in the graphics folder.

•	The main part of the repository holds each of the scripts used in the creation of the outputs. The scripts are listed below, in the order to be completed.

**Steps Taken:**

**Part A–**

•	“Remediation_Buffer.py”  - reads in the remediation sites and the block groups. Builds a 1000-meter buffer around the remediation sites to be used in QGIS. Also dissolves the boundaries so instead of numerous overlapping boundaries, we just have one boundary around all of the overlapping buffers for the sites.

•	The inputs for the “Remediation_Buffer.py” script are the “Remediation_site_borders.shp” file which is taken from the NY State Department of Environmental Conservation, and the block group file from the census. 

•	The output of this file is the “onondaga-remediation.gpkg” file which has three layers. Only the remediation layer will be used in the next script. If you want, you can open QGIS and input the layers to see a map of the block groups of Onondaga County, the remediation boundaries, and a 1000m buffer around those boundaries.

•	“Onondaga_remed_rings.py” – this script creates rings around the remediation sites at 200, 400, 600, 800, 1000, and 2000 meters. It also overlays the tax-parcels on to the aforementioned rings.

•	The inputs for this script are the remediation layer of the just created geopackage file, the block groups from the census, and the tax pacel data (Ask for permission).

•	The outputs for this script are “onondaga_remed_rings.gpkg” which holds the rings around the remediation site, “near_parcels_remed.gpkg” which holds the parcel and ring overlay, and “near_parcels_remediation.csv” dataframe that has each tax parcel with how far they are from the sites.

**Part B – **

•	“Onondaga_bg_demo.py”, “Onondaga_bg_econ.py”, “Onondaga_bg_educ.py” –  these take census data by means of an API call, to make dataframes used in the next three scripts. The first script takes demographic data of the block groups, the second takes median earnings of the block groups, and the third takes education attainment for those over 25 in the block groups.

•	The inputs for these scripts are the data from the census pulled by an API call and the block group file also from the census.

•	The outputs are three dataframes; “Onondaga_bg_demo.csv”, “Onondaga_bg_educ.csv”, and “Onondaga_bg_econ.csv”. Also, three layers added to the “near_parcels_remed.gpkg”; demo_bg, econ_bg, and educ_bg which can be used to make maps based on those three characterisitcs.

**Part C – **

•	“near_remed_demo.py”, “near_remed_educ.py”, and “near_remediation_TAV.py” – The first script creates graphs that looks at the probability of pulling a person of color or a white person at each radius level, and the odds ratio for a person of color living at each radius compared to a white person. The second script creates two graphs that looks at the probability of pulling a person of no college attainment or a person with college attainment at each radius level, and the odds ratio for a person of no college education living at each radius compared to a college educated person. The third script creates a graphic which shows the average total assessed value at each radius level.

•	The input files for the first two are their respective csv files which were created in PART B, “Onondaga_bg_demo.csv”, “Onondaga_bg_educ.csv”, the parcels layer of the “near_parcels_remed.gpkg”, the block group file from the census, and the “class_200_by_bg.csv” file (Ask for permission).

•	The outputs for the first script are the two bar graphs described above: “probs_by_race_remed.png” and “odds_ratio_remed.png”. The second script has the output files: “educ_ratio_remed.png” and “prob_by_educ_remed.png”. The third script has one output file: “avg_tav_radius.png”.

**Part D – **
•	“Onondaga_remed.qgz” – after uploading the layers created throughout the project, one can build several maps which give an overview of the block groups within Onondaga County.

•	The inputs are the “near_parcels_remed.gpkg” and the “Onondaga_remed_rings.gpkg” files

•	The outputs are four maps (three density, and one that shows the tax parcels by total assessed value). More can be created based off of the available data aggregated during this project.

•	Steps: 
o	Add the “block_group” and “remediation” layers of the “Onondaga_remediation.gpkg”
o	Duplicate the block group layer and set the fill pattern to stipes (this will be used later because some of the median earnings data is missing)
o	Add the rings layer from the “Onondaga_remed_ring.gpkg” file.
o	Add the “demo_bg”, “educ_bg”, and “earnings_bg” layers. 
o	To create the density maps for each, use natural breaks.
o	Add the tax parcels  in by pulling the parcels layer of the “near_parcel_remed.gpkg” file
o	Filter down to residential parcels which are those from 200 to 299.
o	Create a natural breaks map using the “TOTAL_AV” variable. 


