import pymongo
import ipdict
import DataFrame
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

cur1 = convertdot(cur[6])
print(cur1)

newdict = ipdict.IPdict(cur1)
newone = newdict.getdict()
ts_url = newdict.ts_URLs
pprint(ts_url)
print(newone)
print("playlists =  ", newdict.length_list)
print("repositories = ", len(cur))

newframe = DataFrame.DataFrame(newone)
newframedict = newframe.read_channels()
myframe = newframe.DataFramee()
myframe.to_csv('file5.csv')

