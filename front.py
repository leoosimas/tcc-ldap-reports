import tkinter as tk
from tkinter import filedialog, Text, ttk,messagebox
import os,ldap3,csv,unicodecsv, re
import sys

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
root.counter = 0

def click_me():

    root.counter += 1

    if var1.get() == 1:
        server= ldap3.Server(serverEntered.get(), port=636, use_ssl=True)
    else:
        server= serverEntered.get()
    
    user= userEntered.get()
    passwd =passwdEntered.get()


    conn = ldap3.Connection(server=server, user=user, password=passwd)

    conn.bind()

    
    if conn.bind() == True:    

        domain = re.split('[@.]',user)

        domain_one = 'dc=' + domain[1]
        domain_two = 'dc=' + domain[2]

        domain = domain_one + ',' + domain_two

        conn.search(domain, '(&(objectclass=person))', attributes=ldap3.ALL_ATTRIBUTES)

        search_result = conn.entries

        print(search_result)

        return search_result
    else:
        conn.unbind()
        tk.messagebox.showerror("Error", "Credenciais inválidas \n Tente novamente \n nº de tentativas restantes " + f'{3 - root.counter}')
        if root.counter == 3:
            root.destroy()
                   
#função para gerar relatório em csv
def generate_me():

    csv_file = filedialog.asksaveasfile(mode='w', defaultextension=".csv") 
    if csv_file is None: 
        return
    fieldnames = ['username',
                  'name',
                  'Logon',
                  'Logoff',
                  'Logon Count'
                    ]

    writer = csv.DictWriter(csv_file,
                            fieldnames=fieldnames)
    writer.writeheader()
    if len(click_me()) > 0:
        for entry in click_me():
            writer.writerow({'username': entry['sAMAccountName'],
                                'name': entry['cn'],
                                'Logon': entry['lastLogon'],
                                'Logoff': entry['lastLogoff'],
                                'Logon Count': entry['logonCount']
                            })

    tk.messagebox.showinfo("LGR - Successfull", "Relatório Gerado")
    

var1 = tk.IntVar()
checkEntered = ttk.Checkbutton(root, text="LDAP over TLS", onvalue = 1, offvalue = 0, variable=var1)
checkEntered.grid(column=2,row=1)

connect = ttk.Button(root, text = "Connect", width=30, command =click_me)
connect.grid(column= 1, row = 4)

generate = ttk.Button(root, text = "Generate", width=30, command =generate_me)
generate.grid(column= 1, row =6)



root.mainloop()