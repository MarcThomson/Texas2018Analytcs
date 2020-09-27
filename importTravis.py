# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 18:41:12 2020

@author: marcw
"""

#Manual importation of Travis County Senate Election Data
#Despair
import pdfplumber
import pandas as pd
pdf =pdfplumber.open("TravisCountyWhy.pdf")

row = 0;
precincts = range(247)
dfSummary = pd.DataFrame(columns={'count'},data=precincts)
dfSummary['precinct'] = ''
dfSummary['DemVotes'] = ''
dfSummary['RepVotes'] = ''
dfSummary['LibVotes'] = ''

for i in range(1235):
    page = pdf.pages[i]
    contents= page.extract_text().split()
    joinedContents = '-'.join(contents)
    if joinedContents.find("Beto")>-1:
        for j in range(len(contents)-1):
            line = contents[j]
            nextline = contents[j+1]
            if (line.find("Beto")>-1) & (nextline.find("O'Rourke")>-1):
                 dfSummary['DemVotes'][row]  = contents[j+7]   
            if (line.find("Ted")>-1) & (nextline.find("Cruz")>-1):
                 dfSummary['RepVotes'][row]  = contents[j+7]      
            if (line.find("Neal")>-1) & (nextline.find("M.")>-1):
                 dfSummary['LibVotes'][row]  = contents[j+8]   
        dfSummary['precinct'][row] = contents[26]
        row+=1

#replace , with ''
for j in range(len(dfSummary)):
    dfSummary['RepVotes'][j] = dfSummary['RepVotes'][j].replace(',', '')
    dfSummary['DemVotes'][j] = dfSummary['DemVotes'][j].replace(',', '')
    dfSummary['LibVotes'][j] = dfSummary['LibVotes'][j].replace(',', '')
    
dfSummary['RepVotes'] = dfSummary['RepVotes'].astype('int')
dfSummary['DemVotes'] = dfSummary['DemVotes'].astype('int')
dfSummary['LibVotes'] = dfSummary['LibVotes'].astype('int')
dfSummary.to_csv('SillyTravis.csv')