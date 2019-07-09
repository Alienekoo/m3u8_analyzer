from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn import metrics
import pandas as pd
import random
import pymongo

conn = pymongo.MongoClient("mongodb://192.168.5.157:27017/")
db = conn.mydatabase_2
col = db.train_data
cur = list(col.find({}, {'_id': False}))
labels = cur[0]['labels']+cur[1]['labels']+ cur[2]['labels']+cur[3]['labels']

data = cur[0]['data']+cur[1]['data']+ cur[2]['data']+cur[3]['data']

col1 = db.channels_train
col2 = db.channels_train
cur2 = list(col2.find({}, {'_id': False}))
channels_train = dict()
for i in range(len(cur2)):
    channels_train.update(cur2[i])
# ================================================================= ML part ============================================================================================


data_train, data_test, labels_train, labels_test = train_test_split(data, labels, test_size=0.33, random_state=42)


clf = RandomForestClassifier(n_estimators=100)
clf.fit(data_train, labels_train)



data_pred = clf.predict(data_test)
score = clf.score(data_test, labels_test)
print("RamdomForest pred: ", data_pred)
print("RandomForest score: ", score)


print("Accuracy with randomForest data: ", metrics.accuracy_score(labels_test, data_pred))


'''for i in range(len(labels_test)):
    for k,v in channels_train.items():
        if v == labels_test[i]:
            print("label is: ", k)
        if v == data_pred[i]:
            print("pred is: ", k)'''



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
