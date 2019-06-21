import socket
import datetime

class IPdict:

    def __init__(self, m3dict):
        self.m3dict = m3dict
        self.tsip = []
        self.m3ip = []
        self.length_list = 0

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
                    v[i] = e, datetime.datetime.now()
            self.tsip.append(socket.gethostbyname(c))
        return v

    def convertip(self, d):
        new = {}
        z = "Unknown"
        for k, v in d.items():
            if isinstance(v, dict):
                v = self.convertip(v)
                # print(k,v)
            # if value is a list
            if isinstance(v, list):
                # print(k, v) d is the value that is being replaced
                if any(isinstance(i, list) for i in v):
                    new['Encryption'] = self.encryption_check(v)
                v = self.convertip_ts(v)

            # if key is url
            if self.verifyurl(k) == True:
                k = str(str(k.split('//', 1)[1]).split('/', 1)[0])
                try:
                    new[socket.gethostbyname(k),datetime.datetime.now()] = v
                    self.m3ip.append(str(socket.gethostbyname(k)))
                except (socket.gaierror, UnicodeError) as e:
                    new[e, datetime.datetime.now()] = v
            else:
                new[k] = v  # if value is just a string

        return new

    def getdict(self):
        newone = {}
        for key, value in self.m3dict.items():
            for vkey, vvalue in value.items():
                newone[key] = {}
                self.length_list += 1
                newone[key][vkey, datetime.datetime.now()] = self.convertip(self.m3dict[key][vkey])
        return newone

    def encryption_check(self, v):
        if len(v[0]) == 4:
            return "yes"
        else:
            return "no"