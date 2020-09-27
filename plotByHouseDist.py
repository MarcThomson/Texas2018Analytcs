# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 21:26:25 2020

@author: marcw
"""

#import geopandas as gpd
#import plotly
#import geojson
#import plotly.express as px

#import packages
import pandas as pd
import numpy as np
import json
from urllib.request import urlopen
import plotly.graph_objects as go

#import summary dataframe
#contents

saveToHtml = False

df =  pd.read_csv("2018ResultsTXByHouseDistrict.csv",dtype={"State House Disctrict": str})


df['text']  = "State House District: " + df['State House Disctrict'] + "<br>" +\
    "Dem State House Margain: " + df['DemLegMargRounded'].astype(str) + "<br>" +\
    "Dem Sen Margain: " +df['DemSenMargRounded'].astype(str) +"<br>"+\
     "Dem Gov Margain: " +df['DemGovMargRounded'].astype(str)


#open json file
with urlopen(' https://opendata.arcgis.com/datasets/0627be7aa6f0440081bd750734761a63_0.geojson') as response:
    gj = json.load(response)

#make a figure containing all traces

traces = []
buttons = []
cols_dd= ['DemSenMarg','DemGovMarg','DemLegMarg']
visible = np.array(cols_dd)

for value in cols_dd:
    traces.append(go.Choroplethmapbox(locations= df['State House Disctrict'],
                                     z=df[value],#np.random.randint(13, 75,  size=L), #synthetic data
                                     colorscale = "RdBu",
                                     text = df['text'] ,
                                     hoverinfo = None,
                                     featureidkey="properties.DIST_NBR",
                                     geojson = gj,
                                     marker_opacity=0.5,
                                     zmin = -80,
                                     zmax = 80,
                                     visible= True if value==cols_dd[0] else False))
    buttons.append(dict(label=value,
                        method="update",
                        args=[{"visible":list(visible==value)},
                              {"title":f"<b>{value}</b>"}]))           


updatemenus = [{"active":0,
                "buttons":buttons,
               }]

#configure figure and show
fig = go.Figure(data=traces,
                layout=dict(updatemenus=updatemenus))
fig .update_layout(mapbox_style="carto-positron",
                  mapbox_zoom=5, mapbox_center = {"lat": 31.2433, "lon": -99.4583},width = 1000,height=1000)
first_title = cols_dd[0]
fig.update_layout(title=f"<b>{first_title}</b>",title_x=0.5)
fig.show()



if saveToHtml:
    import plotly.io as pio
    pio.write_html(fig, file="htmlOutput.html", auto_open=True)


# backup of a working graph 
# Senate win % by state house district
# figSenByHouseDistrict = go.Figure(go.Choroplethmapbox(locations= df['State House Disctrict'],
#                                      z = df['DemSenMargRounded'],#np.random.randint(13, 75,  size=L), #synthetic data
#                                      colorscale = "RdBu",
#                                      text = df['text'] ,
#                                      hoverinfo = None,
#                                      featureidkey="properties.DIST_NBR",
#                                      geojson = gj,
#                                      marker_opacity=0.5,
#                                      zmin = -80,
#                                      zmax = 80,
#                                      visible=True))
# figSenByHouseDistrict.update_layout(mapbox_style="carto-positron",
#                   mapbox_zoom=5, mapbox_center = {"lat": 31.2433, "lon": -99.4583},width = 1000,height=1000)
# figSenByHouseDistrict.show()