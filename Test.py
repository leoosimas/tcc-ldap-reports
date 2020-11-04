import ldap3
from os import path
from getpass import getpass
import sys
import unicodecsv as csv
import csv
import re




host='192.168.1.19'
host = ldap3.Server(host,port=636, use_ssl = True)
user='administrator@tcclab.com'
passwd = '1234Qwer'


conn = ldap3.Connection(host, user=user, password=passwd)

conn.bind()

if conn.bind() == True:
    print("Conectado ao Active Directory")
else:
    print("Credenciais inválidas, tente novamente")

domain = re.split('[@.]',user)

domain_one = 'dc=' + domain[1]
domain_two = 'dc=' + domain[2]

domain = domain_one + ',' + domain_two

conn.search(domain, '(&(objectclass=person))', attributes=ldap3.ALL_ATTRIBUTES)

search_result = conn.entries

for entry in search_result:
    try:
        print(entry['memberOf'])
    except:
        pass



'''with open('report2.csv', mode='w') as csv_file:
    fieldnames = ['username',
                  'name',
                  'Logon',
                  'Logoff'
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
                            })'''
