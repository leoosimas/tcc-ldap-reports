import ldap3
from os import path
from getpass import getpass
import sys
import unicodecsv
import csv



host= input('Server: ')
host = ldap3.Server(host)
user=input('User: ')
passwd = getpass('Password: ')

conn = ldap3.Connection(host, user=user, password=passwd)
conn.bind()

if conn.bind() == True:
    print("Conectado ao Active Directory")
else:
    print("Credenciais inválidas, tente novamente")

conn.search('cn=Users,dc=tcclab,dc=com', '(&(objectclass=person))', attributes=ldap3.ALL_ATTRIBUTES)

search_result = conn.entries

answer = input('Deseja gerar relatório?(Y/N)')

if answer == 'Y':

    with open(input('Nome do arquivo: '), mode='w') as csv_file:
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
else:
    print("Não gerou relatório")