import pymongo
import ipdict

conn = pymongo.MongoClient("mongodb://192.168.5.151:27017/")
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

cur1 = convertdot(cur[0])
print(cur1)

newdict = ipdict.IPdict(cur1)
newone = newdict.getdict()

print("new", newone)


