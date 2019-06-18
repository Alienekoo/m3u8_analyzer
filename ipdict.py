import socket
import datetime

class IPdict:

    def __init__(self, m3dict):
        self.m3dict = m3dict
        self.tsip = []
        self.m3ip = []

    tsip = []
    m3ip = []

    def verifyurl(self, url):
        if 'http' in url:
            return True
        else:
            return False

    def convertip_ts(self, v):
        c = ""
        if any(isinstance(i, list) for i in v):
            for i in range(len(v)):
                v[i][0] = str(str(v[i][0].split('//', 1)[1].split('/', 1)[0]))
                try:
                    b = v[i][0]
                    v[i] = socket.gethostbyname(v[i][0])
                    c = b
                except (socket.gaierror, UnicodeError) as e:
                    # print("Error", e)
                    v[i][0] = str(e), datetime.datetime.now()
            self.tsip.append(socket.gethostbyname(c))
        return v

    def convertip(self, d):
        new = {}
        # print("d is ", d)
        for k, v in d.items():
            if isinstance(v, dict):
                v = self.convertip(v)
                # print(k,v)
            if isinstance(v, list):
                # print(k, v)
                v = self.convertip_ts(v)
                # try:
                # new[k] =socket.gethostbyname(v[i][0]
            if self.verifyurl(k) == True:
                k = str(str(k.split('//', 1)[1]).split('/', 1)[0])
                try:
                    new[socket.gethostbyname(k)] = v
                    self.m3ip.append(str(socket.gethostbyname(k)))
                except (socket.gaierror, UnicodeError) as e:
                    new[str(e), datetime.datetime.now()] = v
            else:
                new[k] = v  # simply replace k with ip if k is a url
        # print("newis ", new)
        return new

    def getdict(self):
        newone = {}
        for key, value in self.m3dict.items():
            for vkey, vvalue in value.items():
                newone[key] = {}
                newone[key][vkey, datetime.datetime.now()] = self.convertip(self.m3dict[key][vkey])
        return newone
