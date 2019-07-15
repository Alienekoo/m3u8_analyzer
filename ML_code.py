from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn import metrics
import numpy as np
from numpy import array
import matplotlib.pyplot as plt
import pandas as pd
import random
from pprint import pprint
import pymongo

def my_hash(line):
    n = 12
    sum = 0
    the_list = [line[i:i + n] for i in range(0, len(line), n)]
    for l in the_list:
        sum += int(l)
    return sum

def convertdot1(d):
    new = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = convertdot1(v)
        new[k.replace('.', '__DOT__')] = v
    return new
conn = pymongo.MongoClient("mongodb://192.168.5.157:27017/")
db = conn.mydatabase_2
col = db.train_data
cur = list(col.find({}, {'_id': False}))
labels = []
data = []
data_test = []
for i in range(len(cur)):
    labels += cur[i]['labels']
    data += cur[i]['data']


# labels = cur[0]['labels']+cur[1]['labels']+cur[2]['labels']+cur[3]['labels']+cur[4]['labels']+cur[5]['labels']
# data = cur[0]['data']+cur[1]['data']+cur[2]['data']+cur[3]['data']+cur[4]['data']+cur[5]['data']

new_data = data
for i in range(len(data)):
    numstr = data[i][9]
    new_data[i][9] = my_hash(numstr) # gives a 13 digit number


col1 = db.test_data
cur1 = list(col1.find({}, {'_id': False}))
for i in range(len(cur1)):
    data_test += cur1[i]['data']


new_data_test = data_test
for i in range(len(data_test)):
    numstr = data_test[i][9]
    new_data_test[i][9] = my_hash(numstr)



col2 = db.channels_train
cur2 = list(col2.find({}, {'_id': False}))


channels_train = dict()
for i in range(len(cur2)):
    channels_train.update(convertdot1(cur2[i]))

# ================================================================= ML part ============================================================================================
'''data_train = new_data
labels_train = labels
data_test = new_data_test
labels_test = cur2[3]'''
data = new_data
data_train, data_test, labels_train, labels_test = train_test_split(data, labels, test_size=0.22, random_state=42)
print(len(data_test), len(labels_train))

clf = RandomForestClassifier(n_estimators=100)
clf.fit(data_train, labels_train)
importances = clf.feature_importances_
data_pred = clf.predict(data_test)
print("RamdomForest pred: ", data_pred)

score = clf.score(data_test, labels_test)
print("RandomForest score: ", score)
for i in range(len(data_test)):
    for k,v in channels_train.items():
        if v == data_pred[i]:
            print("pred is: ", k)
        if v == labels_test[i]:
            print("label is: ", k)

'''


print("Accuracy with randomForest data: ", metrics.accuracy_score(labels_test, data_pred))


data_train = array(data_train)
std = np.std([tree.feature_importances_ for tree in clf.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")

for f in range(data_train.shape[1]):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))

# Plot the feature importances of the forest
plt.figure()
plt.title("Feature importances")
plt.bar(range(data_train.shape[1]), importances[indices],
       color="r", yerr=std[indices], align="center")
plt.xticks(range(data_train.shape[1]), indices)
plt.xlim([-1, data_train.shape[1]])
plt.show()


for i in range(len(data_test)):
    for k,v in channels_train.items():

        if v == data_pred[i]:
            print("pred is: ", k)
        # if v == labels_test[i]:
            # print("label is: ", k)




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
