# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 17:18:45 2020

@author: marcw
"""

import pandas as pd
import numpy as np
import json
from urllib.request import urlopen
import plotly.graph_objects as go
import geopandas as gpd
from os import path
import geojson

# if not(path.exists('ShapeFiles/TX_vtds.geojson')):
#     fp = "ShapeFiles/TX_vtds.shp"
#     map_df = gpd.read_file(fp)
#     map_df = map_df.to_crs(epsg = 4269)
#     map_df.to_file("ShapeFiles/TX_vtds.geojson",driver='GeoJSON')

# with open('ShapeFiles/TX_vtds.geojson') as f:
#     gj = geojson.load(f)

if not(path.exists('Precincts_(1)//Precincts.geojson')):
    fp = "Precincts_(1)//Precincts.shp"
    map_df = gpd.read_file(fp)
    map_df = map_df.to_crs(epsg = 4269)
    map_df.to_file("Precincts_(1)//Precincts.geojson",driver='GeoJSON')

with open('Precincts_(1)//Precincts.geojson') as f:
    gj = geojson.load(f)
    


#df = pd.read_csv("2018ResultsSummaryTXByPrecinct.csv")

df = pd.read_csv("Data/u.s. sen.csv")
df['RepSenVotes'] = df['CruzR_18G_U.S. Sen']
df['DemSenVotes'] =  df["O'RourkeD_18G_U.S. Sen"]
df['LibSenVotes'] = df['DikemanL_18G_U.S. Sen']
df['TotSenVotes'] = df['DemSenVotes'] + df['RepSenVotes'] + df['LibSenVotes'] 
df['%DemSen']=df['DemSenVotes']/df['TotSenVotes']*100
df['%RepSen']=df['RepSenVotes']/df['TotSenVotes']*100
df['DemSenMarg'] = df['%DemSen']-df['%RepSen']
df['DemSenMargRounded'] = round(df['DemSenMarg'],2)
df['DemSenWinner'] = df['DemSenMarg']>0
# precinctList = []
# countyList = []
# IDList = []
# loop = 1
# i=0

# while loop == 1:
#     try:
#         precinctList.append(gj[i]['properties']['VTD'])
#         countyList.append(gj[i]['properties']['COUNTY'])
#         IDList.append(gj[i]['properties']['CNTYVTD'])
#         #a.append(gj[i]['properties']['COUNTY'] + gj[i]['properties']['VTD'])
#     except:
#         loop = 0
#     i+=1 
#     if i>10000:
#         loop=0
# dfTest = pd.DataFrame({'Precinct':precinctList,'County':countyList,'ID':IDList})




fig = go.Figure(go.Choroplethmapbox(locations = df['CNTYVTD'],
                                    z = df['DemSenMargRounded'],
                                    #featureidkey="properties.CNTYVTD",
                                    featureidkey="properties.PCTKEY",
                                    geojson = gj,
                                    colorscale = "RdBu",
                                    marker_opacity=0.5,
                                    zmin = -80,
                                    zmax = 80,
                                    visible= True))
fig .update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=5, mapbox_center = {"lat": 31.2433, "lon": -99.4583},width = 1000,height=1000)
fig.show()



import plotly.io as pio
pio.write_html(fig, file="htmlOutput3.html", auto_open=True)


