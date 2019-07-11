import pymongo
import ipdict
import DataFrame
import pandas as pd
import random
import datetime
from pprint import pprint

conn = pymongo.MongoClient("mongodb://192.168.5.157:27017/")
db = conn.mydatabase
col = db.m3u8_files
cur = list(col.find({}, {'_id': False}))
def convertdot(d):
    new = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = convertdot(v)
        new[k.replace('__DOT__', '.')] = v
    return new

cur1 = convertdot(cur[1])



newdict = ipdict.IPdict(cur1)
newone = newdict.getdict()
# ==================================== dataframe ===================================
if "default_ch0" not in cur1.keys():
    newframe = DataFrame.DataFrame(newone)
    newframedict = newframe.read_channels()
    myframe = newframe.DataFramee()
    myframe.to_csv('file9.csv')


print("playlists =  ", newdict.length_list)
print("repositories = ", len(cur))

# ======================================= ts_url ===================================

ts_url = newdict.ts_URLs
for k,v in ts_url.items():
    if len(v)<100:
        pass
    else:
        ts_url[k] = random.sample(v, 100)

if "default_ch0" not in ts_url.keys():
    ts_url["type"] = "train"
else:
    ts_url["type"] = "test"


def convertdot1(d):
    new = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = convertdot(v)
        new[k.replace('.', '__DOT__')] = v
    return new

ts_url1 = convertdot1(ts_url)
mydb = conn["mydatabase_2"]
mycol = mydb["ts_url"]
x = mycol.insert_one(ts_url1).inserted_id
