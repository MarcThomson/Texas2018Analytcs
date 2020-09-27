# -*- coding: utf-8 -*-
"""
Created on Mon Sep 21 21:00:48 2020

@author: marcw
"""
import pandas as pd

df1 =  pd.read_csv("2018ResultsTXByPrecinct_withTravis_pt1.csv")
df2 =  pd.read_csv("2018ResultsTXByPrecinct_withTravis_pt2.csv")

df = pd.concat([df1,df2])

#filter just the state house rows, get the state house districts
dfStateHouse = df.loc[df['office']=='State House']
stateHouseDistricts = dfStateHouse.district.unique()

#get the unique precinct/county combos
precincts = df.precinct_county.unique()

#build a dictionary linking every precinct/county to its state house district
dictPrecinctStateHouse = {}
rowNum = 0;


for i in range(len(precincts)):
    #check every precinct to see if it occurs in the state house mapping
    dfTemp = dfStateHouse.loc[dfStateHouse['precinct_county']==precincts[i]]
    uniqueTemp = dfTemp.district.unique()
    if(len(uniqueTemp )==1):
        dictPrecinctStateHouse[precincts[i]] = uniqueTemp 
        rowNum+=1
    

#make the dictionary into a pd dataframe, merge with main dataframe
dfPrecinctStateHouse =  pd.DataFrame.from_dict(dictPrecinctStateHouse,orient='index')
dfPrecinctStateHouse = dfPrecinctStateHouse.reset_index()
dfPrecinctStateHouse = dfPrecinctStateHouse.rename(columns = {"index":"precinct_county",0:"State House District"})
df = pd.merge(df, dfPrecinctStateHouse, on='precinct_county')


#create the summary dataframe, iterate through to sum up votes
dfSummary = pd.DataFrame(columns={'State House Disctrict'},data=stateHouseDistricts)
dfSummary['TotSenVotes'] = ''
dfSummary['DemSenVotes'] = ''
dfSummary['RepSenVotes'] = ''
dfSummary['TotGovVotes'] = ''
dfSummary['DemGovVotes'] = ''
dfSummary['RepGovVotes'] = ''
dfSummary['TotLegVotes'] = ''
dfSummary['DemLegVotes'] = ''
dfSummary['RepLegVotes'] = ''

df['votes'] = df['votes'].astype('float')
for i in range(len(stateHouseDistricts)):
    dfSummary['TotSenVotes'][i] = (df.loc[(df['State House District']==stateHouseDistricts[i])&((df['office']=='US Senate'))])['votes'].sum()
    dfSummary['DemSenVotes'][i] = (df.loc[(df['State House District']==stateHouseDistricts[i])&((df['office']=='US Senate'))&(df['party']=='democrat')])['votes'].sum()
    dfSummary['RepSenVotes'][i] = (df.loc[(df['State House District']==stateHouseDistricts[i])&((df['office']=='US Senate'))&(df['party']=='republican')])['votes'].sum()
    dfSummary['TotGovVotes'][i] = (df.loc[(df['State House District']==stateHouseDistricts[i])&((df['office']=='Governor'))])['votes'].sum()
    dfSummary['DemGovVotes'][i] = (df.loc[(df['State House District']==stateHouseDistricts[i])&((df['office']=='Governor'))&(df['party']=='democrat')])['votes'].sum()
    dfSummary['RepGovVotes'][i] = (df.loc[(df['State House District']==stateHouseDistricts[i])&((df['office']=='Governor'))&(df['party']=='republican')])['votes'].sum()
    dfSummary['TotLegVotes'][i] = (df.loc[(df['State House District']==stateHouseDistricts[i])&((df['office']=='State House'))])['votes'].sum()
    dfSummary['DemLegVotes'][i] = (df.loc[(df['State House District']==stateHouseDistricts[i])&((df['office']=='State House'))&(df['party']=='democrat')])['votes'].sum()
    dfSummary['RepLegVotes'][i] = (df.loc[(df['State House District']==stateHouseDistricts[i])&((df['office']=='State House'))&(df['party']=='republican')])['votes'].sum()


#Calculate some summary statistics
dfSummary = dfSummary.sort_values(by='State House Disctrict')

dfSummary['TotSenVotes'] = dfSummary['TotSenVotes'].astype('float')
dfSummary['DemSenVotes'] = dfSummary['DemSenVotes'].astype('float')
dfSummary['RepSenVotes'] = dfSummary['RepSenVotes'].astype('float')
dfSummary['TotGovVotes'] = dfSummary['TotGovVotes'].astype('float')
dfSummary['DemGovVotes'] = dfSummary['DemGovVotes'].astype('float')
dfSummary['RepGovVotes'] = dfSummary['RepGovVotes'].astype('float')
dfSummary['TotLegVotes'] = dfSummary['TotLegVotes'].astype('float')
dfSummary['DemLegVotes'] = dfSummary['DemLegVotes'].astype('float')
dfSummary['RepLegVotes'] = dfSummary['RepLegVotes'].astype('float')

dfSummary['%DemSen']=dfSummary['DemSenVotes']/dfSummary['TotSenVotes']*100
dfSummary['%RepSen']=dfSummary['RepSenVotes']/dfSummary['TotSenVotes']*100
dfSummary['DemSenMarg'] = dfSummary['%DemSen']-dfSummary['%RepSen']
dfSummary['DemSenMargRounded'] = round(dfSummary['DemSenMarg'],2)
dfSummary['DemSenWinner'] = dfSummary['DemSenMarg']>0

dfSummary['%DemGov']=dfSummary['DemGovVotes']/dfSummary['TotGovVotes']*100
dfSummary['%RepGov']=dfSummary['RepGovVotes']/dfSummary['TotGovVotes']*100
dfSummary['DemGovMarg'] = dfSummary['%DemGov']-dfSummary['%RepGov']
dfSummary['DemGovMargRounded'] = round(dfSummary['DemGovMarg'],2)
dfSummary['DemGovWinner'] = dfSummary['DemGovMarg']>0

dfSummary['%DemLeg']=dfSummary['DemLegVotes']/dfSummary['TotLegVotes']*100
dfSummary['%RepLeg']=dfSummary['RepLegVotes']/dfSummary['TotLegVotes']*100
dfSummary['DemLegMarg'] = dfSummary['%DemLeg']-dfSummary['%RepLeg']
dfSummary['DemLegMargRounded'] = round(dfSummary['DemLegMarg'],2)
dfSummary['DemLegWinner'] = dfSummary['DemLegMarg']>0
dfSummary['ContestedLeg'] = (dfSummary['DemLegVotes']>0)& (dfSummary['RepLegVotes']>0)

dfSummary['Target Category']=''
dfSummary.loc[(dfSummary['DemLegWinner']==True)&(dfSummary['DemSenWinner']==True), 'Target Category'] = 'Dem Sweep'
dfSummary.loc[(dfSummary['DemLegWinner']==True)&(dfSummary['DemSenWinner']==False), 'Target Category'] = 'Rep Target'
dfSummary.loc[(dfSummary['DemLegWinner']==False)&(dfSummary['DemSenWinner']==True), 'Target Category'] = 'Dem Target'
dfSummary.loc[(dfSummary['DemLegWinner']==False)&(dfSummary['DemSenWinner']==False), 'Target Category'] = 'Rep Sweep'

dfSummary['DemSenGovCompare'] = dfSummary['DemSenMargRounded'] - dfSummary['DemGovMargRounded']

#save to file
dfSummary.to_csv("2018ResultsTXByHouseDistrict.csv")