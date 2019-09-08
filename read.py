#!/usr/bin/python
# -*- encoding: utf-8 -*-

import json
import sys

def readjson(jsonfile):
    with open(jsonfile, "r") as ffile:
        data = json.load(ffile)

    return data

if __name__ == "__main__":
    data = readjson('/tmp/ssl_get.json')
    
    #data['data'] pois o zbxout é assim. Mudar se necessário
    for d in data['data']:
        if sys.argv[1] == d['{#HOST}']:
            print(d[sys.argv[2]])
