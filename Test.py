import ldap3
from os import path
from getpass import getpass
import sys
import json
import csv
import unicodecsv



host='192.168.1.19'
host = ldap3.Server(host)
user='administrator@tcclab.com'
passwd = '1234Qwer'

conn = ldap3.Connection(host, user=user, password=passwd)
conn.bind()

if conn.bind() == True:
    print("Conectado ao Active Directory")
else:
    print("Credenciais inválidas, tente novamente")

conn.search('cn=Users,dc=tcclab,dc=com', '(&(objectclass=person))', attributes=ldap3.ALL_ATTRIBUTES)

search_result = conn.entries



with open('report2.csv', mode='w') as csv_file:
    fieldnames = ['username',
                  'name',
                  'Logon',
                  'Logoff',
                  ]

    writer = csv.DictWriter(csv_file,
                            fieldnames=fieldnames)
    writer.writeheader()
    if len(search_result) > 0:
        for entry in search_result:
            writer.writerow({'username': entry['sAMAccountName'],
                                'name': entry['cn'],
                                'Logon': entry['lastLogon'],
                                'Logoff': entry['lastLogoff']
                            })
