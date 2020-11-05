import ldap3
from os import path
from getpass import getpass
import sys
import unicodecsv as csv
import csv
import re
import socket

addr1 = socket.gethostbyname('tcclab.com')

if addr1:
    print(True)






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

lista_atributos = ['sAMAccountName','cn', 'title','department','lastLogon','lastLogoff','logonCount','badPwdCount','badPasswordTime','memberof','manager','directReports']

conn.search(domain, '(&(objectclass=person))', attributes=lista_atributos)

search_result = conn.entries

with open('report2.csv', mode='w') as csv_file:
    fieldnames = ['username',
                  'name',
                  'Title',
                  'Department',
                  'Last Logon',
                  'Last Logoff',
                  'Logon Count',
                  'Bad Password Count',
                  'Last Invalid Password',
                  'Member',
                  'manager',
                  'directReports'
                  ]

    writer = csv.DictWriter(csv_file,fieldnames=fieldnames, restval="", extrasaction="ignore")
    writer.writeheader()
    if len(search_result) > 0:
        for entry in search_result:
            writer.writerow({'username': entry['sAMAccountName'],
                                'name': entry['cn'],
                                'Title': entry['title'] if type(entry['title']) is not list else '',
                                'Department': entry['department'] if type(entry['department']) is not list else '',
                                'Last Logon': entry['lastLogon'],
                                'Last Logoff': entry['lastLogoff'],
                                'Logon Count': entry['logonCount'],
                                'Bad Password Count': entry['badPwdCount'],
                                'Last Invalid Password': entry['badPasswordTime'],
                                'Member': entry['memberof']if type(entry['memberof']) is not list else '',
                                'manager': entry['manager']if type(entry['manager']) is not list else '',
                                'directReports':entry['directReports'] if type(entry['directReports']) is not list else ''
                            })

                
               
