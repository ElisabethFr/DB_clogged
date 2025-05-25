'''
main script, still under works
author: Elisabeth Freund
May 25 2025
'''

# this will probably become a function in a module later
# for now, I just want to figure out how to access the DB API and find the stations I want

import requests
import pandas as pd
import json
import os.path
import warnings

cloggeddir = os.path.dirname(__file__)
cloggeddir = 'C:/Users/lisaf/Documents/git/DB_clogged/'

# general urls
fchg_url = "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/fchg/"

# get credentials for DB API access
with open(os.path.join(cloggeddir,'APIkey.json'),'r') as jfile:
    headers = json.loads(jfile.read())
headers.update({"accept": "application/xml"})

# read the EVA_Nos from file
evas = pd.read_parquet(os.path.join(cloggeddir,'stations.parquet'))

# read a list of stations of interest from file
with open(os.path.join(cloggeddir,'stationsofinterest.json'),'r') as jfile:
    stationnames = json.loads(jfile.read())["stations"]

fchg = {}
for s in stationnames:
    try:
        eva = evas.EVA_NO[evas.NAME==s].values[0]
    except IndexError:
        warnings.warn('station ' + s + ' is not in the list of eva numbers. \n \
Check that it is spelled correctly and is a station in Germany. \n \
If an Umlaut is showing up wrong in this error message, try ensuring that stationsofinterest.json is encoded in ANSI. \n \
For further debugging, you can find the existing names in evas')
        continue
    fchg_url_current = fchg_url + str(eva)
    fchg[s] = requests.get(fchg_url_current, headers=headers)
