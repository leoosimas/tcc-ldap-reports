import ldap3
from os import path
from getpass import getpass
import sys
import unicodecsv
import csv



host= input('Server: ')
user=input('User: ')
passwd = getpass('Password: ')
answer = input('Utilizar conexão via LDAPs (LDAP over TLS)? (Y/N) ')

if answer == 'Y':
    host = ldap3.Server(host,port=636, use_ssl = True)
else:
    host = ldap3.Server(host)

conn = ldap3.Connection(host, user=user, password=passwd)

def get_connection(conn):
    conn.bind()

    if conn.bind() == True:
        print("Conectado ao Active Directory")
    else:
        print("Credenciais inválidas, tente novamente")
        
        return 0
    
    return conn.bind()

get_connection(conn)


def get_data():    

    conn.search('cn=Users,dc=tcclab,dc=com', '(&(objectclass=person))', attributes=ldap3.ALL_ATTRIBUTES)

    search_result = conn.entries

    return search_result

search_result = get_data()

def export_csv (search_result):

    answer = input('Deseja gerar relatório?(Y/N)')

    if answer == 'Y':

        with open(input('Nome do arquivo: '), mode='w') as csv_file:
            fieldnames = ['username',
                        'name',
                        'Logon',
                        'Logoff',
                        'Log Count',
                        ]

            writer = csv.DictWriter(csv_file,
                                    fieldnames=fieldnames)
            writer.writeheader()
            if len(search_result) > 0:
                for entry in search_result:
                    writer.writerow({'username': entry['sAMAccountName'],
                                        'name': entry['cn'],
                                        'Logon': entry['lastLogon'],
                                        'Logoff': entry['lastLogoff'],
                                        'Log Count': entry['logonCount']
                                    })
        
        print("Relatório gerado em csv")
    else:
        print("Não gerou relatório")

    return

export_csv(search_result)