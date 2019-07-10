import pymongo
import ipwhois
import socket
from ipwhois import IPWhois
import pandas as pd
from pprint import pprint


class DataFrame:
    def __init__(self, ipdict):
        self.ipdict = ipdict
        self.new_dict = {}



# channel name is the key and value is a dictionary of various attributes
    def read_channels(self):

        for key, value in self.ipdict.items():

            m3ips = set()
            self.new_dict[key] = {}
            self.new_dict[key]['grouptitle'] = []
            self.new_dict[key]['MainM3U8ip'] = ["NONE"]
            self.new_dict[key]['child_m3ips'] = ["NONE"]
            self.new_dict[key]['.ts ips'] = ["NONE"]
            self.new_dict[key]['status'] = "NONE"
            self.new_dict[key]['.ts ips'] = []
            for key1, value1 in value.items():
                self.new_dict[key]['grouptitle'].append(key1)
                for key2, value2 in value1.items():
                    if not isinstance(key2[0], str):
                        self.new_dict[key]['status'] = "Error"
                        continue
                    self.new_dict[key]['MainM3U8ip'].append(key2[0])
                    # if the value2 has child m3 or ts, continue else
                    # print(value2)
                    if not isinstance(value2, dict):
                        self.new_dict[key]['status'] = "Error"
                        continue
                    for key3, value3 in value2.items():
                        # if key3 is a tuple then continue else
                        #print("value2 type: ", type(value2), key3)
                        if isinstance(key3, str):
                            # print("value2 type: ", type(value2), type(key3))
                            self.read_ts(value2, key)
                            continue
                        m3ips.add(key3[0])
                        # print("key is ", key, m3ips)
                        self.new_dict[key]['child_m3ips'] = m3ips
                        #print("type of value3", type(value3))
                        if isinstance(value3, list) or value3 == {}:
                            self.new_dict[key]['status'] = "Error"
                            continue
                        self.read_ts(value3, key)
            self.new_dict[key]['MainM3U8ip'].remove('NONE')
        self.read_asn()
        return self.new_dict

    def read_ts(self,d, key):

        self.new_dict[key]['HLS status'] = d['Encryption']
        self.new_dict[key]['.ts ips'].append(list(set(d['tslist'])))
        if type(d['tslist'][0]) is tuple:
            self.new_dict[key]['.ts ips'] = "ts_Error"
            self.new_dict[key]['status'] = "Error"

    def read_asn(self):
        for key in self.new_dict.keys():
            self.new_dict[key]['ASN_m3u8'] = ["NONE"]
            self.new_dict[key]['ASN_childm3'] = ["NONE"]
            self.new_dict[key]['ASN_ts'] = ["NONE"]
            try:
                if "NONE" not in self.new_dict[key]["MainM3U8ip"]:
                    x = self.new_dict[key]['MainM3U8ip']
                    for ip in x:
                        res = IPWhois(ip).lookup_whois()
                        self.new_dict[key]['ASN_m3u8'].append("AS" + res['asn'])
                        try:
                            self.new_dict[key]['HOST_m3u8'] = socket.gethostbyaddr(ip)
                        except socket.herror as e:
                            self.new_dict[key]['HOST_m3u8'] = "cant reverse lookup"
                    self.new_dict[key]['ASN_m3u8'].remove('NONE')

                if "NONE" not in self.new_dict[key]["child_m3ips"]:
                    y = self.new_dict[key]['child_m3ips']
                    for ip in y:
                        # print(self.new_dict[key]['child_m3ips'])
                        res1 = IPWhois(ip).lookup_whois()
                        self.new_dict[key]['ASN_childm3'].append("AS" + res1['asn'])

                    self.new_dict[key]['ASN_childm3'].remove('NONE')
                if "NONE" not in self.new_dict[key][".ts ips"]:
                    z = self.new_dict[key]['.ts ips']
                    # print (z)
                    for ip in z:
                        res1 = IPWhois(ip[0]).lookup_whois()
                        self.new_dict[key]['ASN_ts'].append("AS" + res1['asn'])
                    self.new_dict[key]['ASN_ts'].remove('NONE')

            except (ipwhois.exceptions.WhoisRateLimitError, ipwhois.exceptions.WhoisLookupError, ipwhois.exceptions.ASNRegistryError, ipwhois.exceptions.HTTPLookupError) as e:
                self.new_dict[key]['status'] = str(e)

    def DataFramee(self):
        self.new_dict = self.read_channels()
        # pprint(self.new_dict)
        df = pd.DataFrame.from_dict(self.new_dict, orient='index')
        return df

    def get_hostname(self):
        self.new_dict