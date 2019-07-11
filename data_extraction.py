import pymongo
import urllib.parse as urlparse
import random
from string import ascii_lowercase
import pandas as pd
from random import randint
import math
# ============================================================== data extraction =======================================================================================
conn = pymongo.MongoClient("mongodb://192.168.5.157:27017/")
mydb = conn.mydatabase_2
myts = mydb.ts_url
cur = list(myts.find({}, {'_id': False}))


LETTERS = {letter: str(index) for index, letter in enumerate(ascii_lowercase, start=1)}

def convertToNumber (s):
    return int.from_bytes(s.encode(), 'little')

def convertFromNumber (n):
    return n.to_bytes(math.ceil(n.bit_length() / 8), 'little').decode()


def convertdot(d):
    new = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = convertdot(v)
        new[k.replace('__DOT__', '.')] = v
    return new

def convertdot1(d):
    new = {}
    for k, v in d.items():
        if isinstance(v, dict):
            v = convertdot1(v)
        new[k.replace('.', '__DOT__')] = v
    return new

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def alphabet_position(text):
    text = text.lower()

    numbers = [LETTERS[character] for character in text if character in LETTERS]

    z = ' '.join(numbers)
    return int(z.replace(" ", ""))



def getDataAndLabelsTrain(ts_url):
    labels = []
    data = []
    channels = dict()
    urls = dict()
    s0 = ''
    for k, v in ts_url.items():

        counter = str(alphabet_position(k))
                  # + int(str(alphabet_position(k))[:5])

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
                    s0 = 'dump1'
                else:
                    counter2 = str(convertToNumber(s0))
                    netloc_status = counter2

                s1 = urlparse.urlsplit(v[i]).path
                path_ascii = [ord(c) for c in s1]
                a_list = [0] * 128
                for j in path_ascii:
                    a_list[j] += 1
                line = ''.join(map(str, a_list))
                print(len(line))
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

        # print("s0 is ", s0)
            urls[s0] = counter2
        channels[k] = counter

    data_dict = {'labels': labels, 'data': data}
    mycol = mydb["train_data"]
    x = mycol.insert_one(data_dict).inserted_id
    mycol1 = mydb["channels_train"]
    y = mycol1.insert_one(convertdot1(channels)).inserted_id
    mycol2 = mydb["urls_train"]
    z = mycol2.insert_one(convertdot1(urls)).inserted_id

def getDataTrain(ts_url):
    myurls = mydb.urls_train
    cur2 = list(myurls.find({}, {'_id': False}))
    urls_train = dict()
    for i in range(len(cur2)):
        urls_train.update(convertdot(cur2[i]))

    data = []
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
                if s0 in urls_train.keys():
                    netloc_status = urls_train[s0]
                    s0 = 'dump1'
                elif s0 in urls.keys():
                    netloc_status = urls[s0]
                    s0 = 'dump1'
                else:
                    counter2 = str(convertToNumber(s0))
                    netloc_status = counter2

                s1 = urlparse.urlsplit(v[i]).path
                path_ascii = [ord(c) for c in s1]
                a_list = [0] * 128
                for j in path_ascii:
                    a_list[j] += 1
                line = ''.join(map(str, a_list))
                print(len(line))
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

        # print("s0 is ", s0)
            urls[s0] = counter2
    data_dict = {'data': data}
    mycol = mydb["test_data"]
    x = mycol.insert_one(data_dict).inserted_id
    mycol2 = mydb["urls_train"]
    z = mycol2.insert_one(convertdot1(urls)).inserted_id


# ts_url = convertdot(cur[len(cur)-1])

for i in range(len(cur)):
    ts_url = convertdot(cur[i])
    if ts_url['type'] == "train":
        ts_url.pop('type', None)
        getDataAndLabelsTrain(ts_url)
    elif ts_url['type'] == 'test':
        ts_url.pop('type', None)
        getDataTrain(ts_url)
    else:
        print("Invalid file")

























# print(channels_train)

# feature_imp = pd.Series(clf.feature_importances_, index=headings)
# datapd = pd.DataFrame.from_records(data, columns=headings)
# print(datapd.head())


