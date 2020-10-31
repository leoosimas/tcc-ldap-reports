import ldap3
from os import path
from getpass import getpass
import sys
import json
import csv



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

data = []

for entry in conn.entries:
   data.append(entry)

with open('report.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     wr.writerow(data)
