import pymongo
import ipdict
import DataFrame
import urllib.parse as urlparse
from sklearn.ensemble import RandomForestClassifier
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

cur1 = convertdot(cur[6])
print(cur1)

newdict = ipdict.IPdict(cur1)
newone = newdict.getdict()
ts_url = newdict.ts_URLs

print("playlists =  ", newdict.length_list)
print("repositories = ", len(cur))

newframe = DataFrame.DataFrame(newone)
newframedict = newframe.read_channels()
myframe = newframe.DataFramee()
myframe.to_csv('file6.csv')


def getDataAndLabelsTest(ts_url):
    labels = []
    data = []
    counter = 0
    counter2 = 0
    channels = dict()
    urls = dict()
    s0 = ''
    for k, v in ts_url.items():
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
            else:
                netloc_status = counter2
                s0 = 'dump'

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
        urls[s0] = counter2
        channels[k] = counter
        counter += 1
        counter2 += 1
    headings = [http_status, netloc_status, path_status_1, path_status_2, path_status_3, path_status_4, path_status_5,
                path_status_6, query_status, fragment_status]
    return data, labels, channels, urls, headings

data_train, labels_train, channels_train, urls_train, headings = getDataAndLabelsTest(ts_url)


datapd = pd.DataFrame.from_records(data_train, columns=headings)
print(datapd.head())
print(labels_train)
print(data_train)


clf = RandomForestClassifier(n_estimators=100)
clf.fit(data_train, labels_train)
RandomForestClassifier(bootstrap=True,class_weight=None, criterion='gini',max_depth=None,
                       max_features='auto',max_leaf_nodes=None,
                       min_samples_leaf=1, min_samples_split=2,
                       min_weight_fraction_leaf=0.0, n_estimators=100, n_jobs=1,
                       oob_score=False, random_state=None, verbose=0,
                       warm_start=False)

feature_imp = pd.Series(clf.feature_importances_, index=headings)

test_urls = dict()
test_list = random.sample(ts_url.items(), 30)
for i in range(len(test_list)):
    test_urls[test_list[i][0]] = test_list[i][1]
print(test_urls)


def getDataAndLabelsTrain(test_urls, urls_traina, channels_traina):
    labels = []
    data = []
    for k, v in test_urls.items():
        for i in range(len(v)):
            if urlparse.urlsplit(v[i]).scheme == 'http':
                http_status = 1
            elif urlparse.urlsplit(v[i]).scheme == 'https':
                http_status = 2
            else:
                http_status = 0
            s0 = urlparse.urlsplit(v[i]).netloc
            if s0 in urls_train.keys():
                netloc_status = urls_traina[s0]
            else:
                netloc_status = 99999999
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
            if k in channels_train.keys():
                labels.append(channels_traina[k])
            else:
                labels.append(99999999)

    headings = [http_status, netloc_status, path_status_1, path_status_2, path_status_3, path_status_4, path_status_5,
                path_status_6, query_status, fragment_status]

    return data, labels, headings


data_test, labels_test, headings_test = getDataAndLabelsTrain(test_urls, urls_train, channels_train)

data_pred = clf.predict(data_test)

from sklearn import metrics

print("Accuracy with random test data: ", metrics.accuracy_score(labels_test, data_pred))


'''data_dict = {'labels' : labels, 'data' : data}
mydb = conn["mydatabase_2"]
mycol = mydb["train_data"]
x = mycol.insert_one(data_dict).inserted_id'''

