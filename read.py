#!/usr/bin/python
# -*- encoding: utf-8 -*-

import json
import sys

if __name__ == "__main__":
    with open('/tmp/ssl_get.json','r') as jsonfile:
        data = json.load(jsonfile)
        chave = sys.argv[2]
        chave = chave.upper()
        chave = "{#%s}" %chave
    
        #data['data'] pois o zbxout é assim. Mudar se necessário
        for d in data['data']:
            if sys.argv[1] == d['{#HOST}']:
                print(d[chave])
