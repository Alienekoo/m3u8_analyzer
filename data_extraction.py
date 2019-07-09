import pymongo
import urllib.parse as urlparse
import random
from string import ascii_lowercase
import pandas as pd
# ============================================================== data extraction =======================================================================================
conn = pymongo.MongoClient("mongodb://192.168.5.157:27017/")
mydb = conn.mydatabase_2
myts = mydb.ts_url
cur = list(myts.find({}, {'_id': False}))
ts_url = cur[4]

LETTERS = {letter: str(index) for index, letter in enumerate(ascii_lowercase, start=1)}

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

        counter = alphabet_position(k) %10000000000

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


    headings = [http_status, netloc_status, path_status_1, path_status_2, path_status_3, path_status_4, path_status_5,
                path_status_6, query_status, fragment_status]
    return data, labels, channels, urls, headings

data, labels, channels_train, urls_train, headings = getDataAndLabelsTrain(ts_url)

print(channels_train)

# feature_imp = pd.Series(clf.feature_importances_, index=headings)
# datapd = pd.DataFrame.from_records(data, columns=headings)
# print(datapd.head())


data_dict = {'labels' : labels, 'data' : data}
mycol = mydb["train_data"]
x = mycol.insert_one(data_dict).inserted_id
mycol1 = mydb["channels_train"]
y = mycol1.insert_one(channels_train).inserted_id
