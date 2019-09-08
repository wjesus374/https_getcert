# HTTPS Get Cert (for Zabbix LLD)
Python Script to get HTTPS Info

Para utilização do script, colocar os *.py* em qualquer diretório que o Agente do Zabbix tenha permissão de execução.

Preencher os host's com o DNS e porta que você deseja coletar os certificados.

<pre>
hostdict = [
        {'host': 'www.google.com.br', 'port': '443'},
        {'host': 'www.uol.com.br', 'port': '443'}
        ]
</pre>

Configurar o UserParameter, dessa forma:

<pre>
UserParameter=get_ssl,/opt/zabbix/scripts/get_ssl_info.py
UserParameter=read[*],/opt/zabbix/scripts/read.py $1 $2
</pre>

Reiniciar o agente

Na interface web do Zabbix

Configurar um host e adicionar a descoberta com os parametros:

* Qualquer nome
* Tipo = Agente Zabbix
* Interface do host que estiver configurado
* Atualização = 300s
* Período de retenção de itens perdidos = 0

Os *protótipos de itens* serão do tipo *Agente Zabbix*, a chave terá que ser read[{#HOST},seconds] para monitorar os segundos restantes para expiração do certificado. O restante dos parametros, fica ao seu critério.

É possível monitorar qualquer outro valor que tenha uma chave válida, para saber todas as chaves, olhar o arquivo */tmp/ssl_get.json*:

Exemplo:
<pre>
            "{#CAISSUERS}": "http://pki.goog/gsr2/GTS1O1.crt",
            "{#CRLDISTRIBUTIONPOINTS}": "http://crl.pki.goog/GTS1O1.crl",
            "{#HOST}": "www.google.com.br",
            "{#ISSUER_COMMONNAME}": "GTS CA 1O1",
            "{#ISSUER_COUNTRYNAME}": "US",
            "{#ISSUER_ORGANIZATIONNAME}": "Google Trust Services",
            "{#NOTAFTER}": "Nov 21 10:28:57 2019 GMT",
            "{#NOTBEFORE}": "Aug 23 10:28:57 2019 GMT",
            "{#OCSP}": "http://ocsp.pki.goog/gts1o1",
            "{#PORT}": 443,
            "{#SECONDS_STR}": "73 days, 17:47:37",
            "{#SECONDS}": 6371257.0,
            "{#SERIALNUMBER}": "4F4A4ECF8B0E8975080000000011BB69",
            "{#SUBJECT_COMMONNAME}": "*.google.com",
            "{#SUBJECT_COUNTRYNAME}": "US",
            "{#SUBJECT_LOCALITYNAME}": "Mountain View",
            "{#SUBJECT_ORGANIZATIONNAME}": "Google LLC",
            "{#SUBJECT_STATEORPROVINCENAME}": "California",
            "{#VERSION}": 3
</pre>

Obs. As chaves poderão ser em CAIXA ALTA ou em caixa baixa. O importante é colocar o nome da chave corretamente.
