#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import socket
import ssl
from datetime import datetime, timedelta
import json
import types

hostdict = [ 
        {'host': 'www.google.com.br', 'port': '443'}, 
        {'host': 'www.uol.com.br', 'port': '443'}
        ]

def writejson(configfile,data):

    with open(configfile,"w", encoding="utf8") as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4, sort_keys=True)

def getcert(host,port):
    #Criar contexto SSL
    ctx = ssl.create_default_context()
    s = ctx.wrap_socket(socket.socket(), server_hostname=host)
    #Timeout to host
    s.settimeout(3.0)

    try:
        #Conectar no host
        s.connect((host, port))
        cert = s.getpeercert()
    except:
        return "Erro ao conectar no host %s" %host

    #Dict com os dados para return
    data = {}

    notafter = cert['notAfter']
    #Verifique o formato do notafter descomentando
    #print(notafter)
    #Ajuste para o formato que aparece no console
    FMT = '%b %d %H:%M:%S %Y GMT'
    now = datetime.now().strftime(FMT)
    #notafter = notafter.decode('utf-8')

    #Converter a string em objeto datetime
    #Coletar as informações do datetime de agora
    tn = datetime.strptime(now,FMT)
    #Coletar as informações do datetime do notafter
    ta = datetime.strptime(notafter,FMT)

    #Subtração da data "notafter" com a data atual
    td = ta - tn
    seconds = td.total_seconds()

    #Mostrar a diferença em segundos
    #print(seconds)

    #Mostrar a diferença em string
    #print(str(td))

    data['seconds'] = []
    data['seconds'].append(seconds)

    data['seconds_str'] = []
    data['seconds_str'].append(str(td))

    try:
        for info in cert:
            data[info] = []
            #print("========"+info)
            if isinstance(cert[info], tuple):
                try:
                    #print("========"+info)
                    value = dict(x[0] for x in cert[info])
                    data[info].append(value)
                    #print(type(value))
                except:
                    #print("========"+info)
                    for x in cert[info]:
                        data[info].append(x)
            else:
                data[info].append(cert[info])

        return data
    except Exception as e:
        data['error'] = []
        data['error'].append(e)
        #return "Erro ao processar os valores: %s" %e
        return data


if __name__ == "__main__":

    #Output LLD para o Zabbix
    zbxout = {}
    zbxout['data'] = []

    
    for info in hostdict:
        host = info['host']
        port = int(info['port'])
        result = getcert(host,port)

        #Dict para {#CHAVE} e valor
        stat= {}

        for i in result:
            if isinstance(result[i], list):
                #Eu sei, tenho achar nomes melhores para as variáveis :P
                num = 1
                for d in result[i]:
                    #Se for dict, provavelmente são as entradas SUBJECT e ISSUER
                    if isinstance(d, dict):
                        for p in d:
                            chave = "%s_%s" %(i,p)
                            chave = chave.upper()
                            chave = "{#%s}" %(chave)
                            stat[chave] = d[p]
                    #Se for tuple, provavelmente são as entradas de DNS
                    elif isinstance(d, tuple):
                        #Decomentar se for utilizar :)
                        pass
                        #chave = "%s_%s" %(d[0],num)
                        #chave = chave.upper()
                        #chave = "{#%s}" %(chave)
                        #stat[chave] = d[1]
                        #num += 1
                    else:
                        #print(d)
                        chave = i.upper()
                        chave = "{#%s}" %chave
                        stat[chave] = d

        #Dados finais para completar o zbxout
        stat['{#HOST}'] = host
        stat['{#PORT}'] = port
        zbxout['data'].append(stat)
    print(json.dumps(zbxout))
    #Gravar dados para o read.py
    writejson('/tmp/ssl_get.json',zbxout)
