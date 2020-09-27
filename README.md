# Analytics of the 2018 Texas Elections


Python Scripts:
 - importTravis.py reads the pdf 'TravisCountyWhy.pdf' and extracts the senate election results
 - mergeTravis.py merges this dataset with the MIT 2018 election data by precinct (too large for github)
 -- The output of mergeTravis.py are the "2018Results..." csv's. These files are the same dataframe split for size constainsts, and contain precinct-level election data
 - AggregateDataByStateHouseDist.py aggregates the data by state house district in the csv 2018ResultsTXByHouseDistrict.csv
 - plotByHouseDistrict.py plots the election results onto a shape file of the state house districts, with the option of outputting to html


Sources:
 - Most election data: https://electionlab.mit.edu/data
 - Supplemental data for Travis County: https://countyclerk.traviscountytx.gov/images/pdfs/election_results/20181106pct1.pdf
 - Shapefiles for districts, counties: https://gis-txdot.opendata.arcgis.com/search
 - Shapefile for precincts: https://github.com/mggg-states/TX-shapefiles
