# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 12:38:15 2020

@author: marcw
"""

#One time script needed to merge Travis county senate data (SillyTravis.csv) with main file
#Travis county senate data was absent for reasons unexplained
#SillyTravis.csv was built using importTravis.py
import pandas as pd


df =  pd.read_csv("2018ResultsTXByPrecinct.csv") #This file was made using MIT data, which is too large to put on github

dfTravis = pd.read_csv("SillyTravis.csv")

for i in range(len(dfTravis)):
    #democratic votes
    demIndex = df.loc[(df['county']=='Travis') &\
                              (df['precinct']==dfTravis['precinct'][i].astype('int').astype('str'))&\
                                  (df['office']=='US Senate')&\
                                     (df['party']=='democrat')].index
    df['votes'][demIndex] = dfTravis['DemVotes'][i]
                                      
    #republican votes
    repIndex = df.loc[(df['county']=='Travis') &\
                              (df['precinct']==dfTravis['precinct'][i].astype('int').astype('str'))&\
                                  (df['office']=='US Senate')&\
                                     (df['party']=='republican')].index
        
    df['votes'][repIndex] = dfTravis['RepVotes'][i]
    #libertarian votes
    libIndex = df.loc[(df['county']=='Travis') &\
                              (df['precinct']==dfTravis['precinct'][i].astype('int').astype('str'))&\
                                  (df['office']=='US Senate')&\
                                     (df['party']=='libertarian')].index
    df['votes'][libIndex] = dfTravis['LibVotes'][i]


#save separately for file size to work
Nsplit = round(len(df)/2)
dfPart1 = df[0:Nsplit]
dfPart2 = df[Nsplit+1:]
dfPart1.to_csv('2018ResultsTXByPrecinct_withTravis_pt1.csv')
dfPart2.to_csv('2018ResultsTXByPrecinct_withTravis_pt2.csv')