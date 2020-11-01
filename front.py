import tkinter as tk
from tkinter import filedialog, Text
from tkinter import ttk
import os
import ldap3
import csv
import unicodecsv


root = tk.Tk()

root.title("LDAP REPORT GENERATOR")
root.minsize(300,150)


label = ttk.Label(root,text='LDAP REPORT GENERATOR')
label.grid(column=1,row=0)

label = ttk.Label(root,text='Server')
label.grid(column=0,row=1)

label1 = ttk.Label(root,text='User')
label1.grid(column=0,row=2)

label2 = ttk.Label(root,text='Password')
label2.grid(column=0,row=3)


serverEntered = ttk.Entry(root, width = 30)
serverEntered.grid(column=1,row=1)


userEntered = ttk.Entry(root, width = 30)
userEntered.grid(column=1,row=2)


passwdEntered = ttk.Entry(root,show = "*", width = 30)
passwdEntered.grid(column=1,row=3)


#função para conectar via ldap e puxar todos as informações do Active Directory
def click_me():

    server= serverEntered.get()
    user= userEntered.get()
    passwd =passwdEntered.get()

    print(server,user,passwd)

    conn = ldap3.Connection(server=server, user=user, password=passwd)

    conn.bind()

    conn.search('cn=Users,dc=tcclab,dc=com', '(&(objectclass=person))', attributes=ldap3.ALL_ATTRIBUTES)

    search_result = conn.entries

    print(search_result)
    
    
    return search_result

#função para gerar relatório em csv
def generate_me():

    csv_file = filedialog.asksaveasfile(mode='w', defaultextension=".csv") 
    if csv_file is None: 
        return
    fieldnames = ['username',
                  'name',
                  'Logon',
                  'Logoff',
                    ]

    writer = csv.DictWriter(csv_file,
                            fieldnames=fieldnames)
    writer.writeheader()
    if len(click_me()) > 0:
        for entry in click_me():
            writer.writerow({'username': entry['sAMAccountName'],
                                'name': entry['cn'],
                                'Logon': entry['lastLogon'],
                                'Logoff': entry['lastLogoff']
                            })




connect = ttk.Button(root, text = "Connect", width=30, command =click_me)
connect.grid(column= 1, row = 4)
generate = ttk.Button(root, text = "Generate", width=30, command =generate_me)
generate.grid(column= 1, row =5)



root.mainloop()