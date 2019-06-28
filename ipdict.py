import socket
import datetime
from pprint import pprint
class IPdict:

    def __init__(self, m3dict):
        self.m3dict = m3dict
        self.tsip = []
        self.ts_URLs = dict()
        self.length_list = 0


    def verifyurl(self, url):
        if 'http' in url:
            return True
        else:
            return False

    def convertip_ts(self, v, c1):
        c = ""

        if any(isinstance(i, list) for i in v):
            for i in range(len(v)):
                c = v[i][0]
                v[i][0] = str(str(v[i][0].split('//', 1)[1].split('/', 1)[0]))
                try:
                    b = socket.gethostbyname(v[i][0])
                    v[i] = b
                except (socket.gaierror, UnicodeError) as e:
                    # print("Error", e)
                    v[i] = e, datetime.datetime.now()
                c1.append(c)
        self.tsip.extend(c1)
        return v

    def convertip(self, d, c1):
        new = {}
        self.tsip = []
        z = "Unknown"
        for k, v in d.items():
            if isinstance(v, dict):
                v = self.convertip(v, c1)
                # print(k,v)
            # if value is a list

            if isinstance(v, list):
                # print(k, v) d is the value that is being replaced
                if any(isinstance(i, list) for i in v):
                    new['Encryption'] = self.encryption_check(v)
                v = self.convertip_ts(v, c1)

            # if key is url
            if self.verifyurl(k) == True:
                k = str(str(k.split('//', 1)[1]).split('/', 1)[0])
                try:
                    new[socket.gethostbyname(k),datetime.datetime.now()] = v
                except (socket.gaierror, UnicodeError) as e:
                    new[e, datetime.datetime.now()] = v
            else:
                new[k] = v  # if value is just a string

        return new

    def getdict(self):
        newone = {}
        for key, value in self.m3dict.items():
            newone[key] = {}
            for vkey, vvalue in value.items():
                c1 = []
                self.length_list += 1
                #print(vkey)
                newone[key][vkey] = self.convertip(self.m3dict[key][vkey], c1)
                # print("tsip is", key, self.tsip)
                self.ts_URLs[key] = self.tsip

        return newone

    def encryption_check(self, v):
        if len(v[0]) == 4:
            return "yes"
        else:
            return "no"