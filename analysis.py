import pymongo
import ipdict
import DataFrame
import urllib.parse as urlparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
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

cur1 = convertdot(cur[9])

newdict = ipdict.IPdict(cur1)
newone = newdict.getdict()
ts_url = newdict.ts_URLs

print("playlists =  ", newdict.length_list)
print("repositories = ", len(cur))

newframe = DataFrame.DataFrame(newone)
newframedict = newframe.read_channels()
myframe = newframe.DataFramee()
myframe.to_csv('file6.csv')
pprint(ts_url)

# ============================================================== data extraction =======================================================================================

def getDataAndLabelsTrain(ts_url):
    labels = []
    data = []
    counter = 0
    channels = dict()
    urls = dict()
    s0 = ''
    for k, v in ts_url.items():
        if v == []:
            s0 = 'dump'
        else:
            for i in range(len(v)):

                if urlparse.urlsplit(v[i]).scheme == 'http':
                    http_status = 1
                elif urlparse.urlsplit(v[i]).scheme == 'https':
                    http_status = 2
                else:
                    http_status = 0

                s0 = urlparse.urlsplit(v[i]).netloc
                if s0 in urls.keys():
                    netloc_status = urls[s0]
                    s0 = 'dump'
                else:
                    netloc_status = counter

                s1 = urlparse.urlsplit(v[i]).path
                path_ascii = [ord(c) for c in s1]
                a_list = [0] * 128
                for j in path_ascii:
                    a_list[j] += 1
                line = ''.join(map(str, a_list))
                n = 16
                the_list = [line[i:i + n] for i in range(0, len(line), n)]
                path_status_1 = int(the_list[2])
                path_status_2 = int(the_list[3])
                path_status_3 = int(the_list[4])
                path_status_4 = int(the_list[5])
                path_status_5 = int(the_list[6])
                path_status_6 = int(the_list[7])

                s2 = urlparse.urlsplit(v[i]).query
                query_ascii = [ord(c) for c in s2]
                if query_ascii == []:
                    s = 0
                else:
                    s = 1
                query_status = int(s)

                s3 = urlparse.urlsplit(v[i]).fragment
                fragment_ascii = [ord(c) for c in s3]
                if fragment_ascii == []:
                    s = 0
                else:
                    s = 1
                fragment_status = int(s)

                split_list = [http_status, netloc_status, path_status_1, path_status_2, path_status_3, path_status_4,
                              path_status_5, path_status_6, query_status, fragment_status]
                data.append(split_list)
                labels.append(counter)

        print("s0 is ", s0)
        urls[s0] = counter
        channels[k] = counter
        counter += 1

    headings = [http_status, netloc_status, path_status_1, path_status_2, path_status_3, path_status_4, path_status_5,
                path_status_6, query_status, fragment_status]
    return data, labels, channels, urls, headings

data, labels, channels_train, urls_train, headings = getDataAndLabelsTrain(ts_url)

# datapd = pd.DataFrame.from_records(data, columns=headings)
# print(datapd.head())

# ================================================================= ML part ============================================================================================


data_train, data_test, labels_train, labels_test = train_test_split(data, labels, test_size=0.33, random_state=42)


clf = RandomForestClassifier(n_estimators=100)
clf.fit(data_train, labels_train)

feature_imp = pd.Series(clf.feature_importances_, index=headings)

data_pred = clf.predict(data_test)
score = clf.score(data_test, labels_test)
print("RamdomForest pred: ", data_pred)
print("RandomForest score: ", score)
from sklearn import metrics

print("Accuracy with randomForest data: ", metrics.accuracy_score(labels_test, data_pred))

'''

lr = LogisticRegression(solver='lbfgs', multi_class='auto', max_iter=10000)
lr.fit(data_train, labels_train)
predictions = lr.predict(data_test)
score = lr.score(data_test, labels_test)
print("logistic pred: ", predictions)
print("logistic score: ", score)



dtc = DecisionTreeClassifier()
dtc.fit(data_train, labels_train)
predictions = dtc.predict(data_test)
score = dtc.score(data_test, labels_test)
print("decision pred: ", predictions)
print("decision score: ", score)


svm = svm.SVC(gamma='auto', C=1, kernel='linear')
svm.fit(data_train, labels_train)
predictions = svm.predict(data_test)
score = svm.score(data_test, labels_test)
print("svm pred: ", predictions)
print("svm score: ", score)

'''




data_dict = {'labels' : labels, 'data' : data}
mydb = conn["mydatabase_2"]
mycol = mydb["train_data"]
x = mycol.insert_one(data_dict).inserted_id

