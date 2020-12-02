import tkinter as tk
from tkinter import filedialog, Text, ttk,messagebox
import tkinter.font as font
import os,ldap3,csv,unicodecsv, re
import sys

root = tk.Tk()

photo = tk.PhotoImage(file = "ldap.png")
root.iconphoto(False, photo)

root.title("LDAP REPORT GENERATOR")
root.minsize(300,150)


label = ttk.Label(root,text='LDAP REPORT GENERATOR',font='Calibri 14 bold')
label.grid(column=1,row=0,pady=6)

label = ttk.Label(root,text='Server', font='Calibri 10 bold')
label.grid(column=0,row=1,padx=8, sticky='W')


label1 = ttk.Label(root,text='User',font='Calibri 10 bold' )
label1.grid(column=0,row=2,padx=8,sticky='W')

label2 = ttk.Label(root,text='Password', font='Calibri 10 bold')
label2.grid(column=0,row=3,padx=8,sticky='W')


serverEntered = ttk.Entry(root, width = 30)
serverEntered.grid(column=1,row=1,pady=2)

userEntered = ttk.Entry(root, width = 30)
userEntered.grid(column=1,row=2,pady=2)

passwdEntered = ttk.Entry(root,show = "*", width = 30)
passwdEntered.grid(column=1,row=3,pady=2)



root.counter = 0


#função para conectar via ldap e puxar todos as informações do Active Directory
def click_me():

    

    global search_result


    if var1.get() == 1:
        server= ldap3.Server(serverEntered.get(), port=636, use_ssl=True)
    else:
        server= serverEntered.get()
    
    user= userEntered.get()
    passwd =passwdEntered.get()

    if user == '' or server == '' or passwd == '':
        tk.messagebox.showerror("LGR - Error", "Um ou mais campos estão em branco \npor favor preencher para conectar ao Active Directory")
    else:

        domain = re.split('[@.]',user)

        

        if domain[0] != 'administrator':
            root.counter += 1
            tk.messagebox.showerror("LGR - Error", "Apenas o user Admin deste domínio \npode conectar e requistar os dados \nTentativas restantes " f'{3 - root.counter}') 
            if root.counter == 3:
                root.destroy()
        else:
            conn = ldap3.Connection(server=server, user=user, password=passwd)
            conn.bind()  

        
            if conn.bind() == True:   

                
                tk.messagebox.showinfo("LGR - Connected", "Conectado ao Active Directory") 

                serverEntered.delete(0, tk.END)
                userEntered.delete(0, tk.END)
                passwdEntered.delete(0, tk.END)


                domain_one = 'dc=' + domain[1]
                domain_two = 'dc=' + domain[2]

                domain = domain_one + ',' + domain_two

                if var2.get() == 1:

                    lista_atributos = ['sAMAccountName','cn', 'title','department','lastLogon','lastLogoff','logonCount','badPwdCount','badPasswordTime','memberof','manager','directReports','userPrincipalName','telephoneNumber','whenCreated','whenChanged','dSCorePropagationData','company','objectClass', 'objectCategory','accountExpires']
                else:
                    lista_atributos = ['sAMAccountName','cn','title','userPrincipalName','telephoneNumber','department','lastLogon','logonCount','memberof','manager']

                conn.search(domain, '(&(objectclass=person))', attributes=lista_atributos)

                search_result = conn.entries

                return search_result      
            else:
                conn.unbind()
                root.counter += 1
                tk.messagebox.showerror("LGR - Error", "Credenciais inválidas \n Tente novamente \n nº de tentativas restantes " + f'{3 - root.counter}')
                if root.counter == 3:
                    root.destroy()


#função para gerar relatório em csv
def generate_me():

    print(search_result)
    

    csv_file = filedialog.asksaveasfile(mode='w', defaultextension=".csv") 
    if csv_file is None: 
        return
    if var2.get()==1:
        
        fieldnames = ['Company', 
                    'Username',
                    'Name',
                    'Title',
                    'Email',
                    'Telephone',
                    'Department',
                    'Manager',
                    'Last Logon',
                    'Last Logoff',
                    'Logon Count',
                    'Bad Password Count',
                    'Last Invalid Password',
                    'Member',
                    'Direct Reports',
                    'Created in',
                    'Last Change',
                    'Object Class',
                    'Account Expires'
                        ]

        writer = csv.DictWriter(csv_file,
                                fieldnames=fieldnames)
        writer.writeheader()
        if len(search_result) > 0:
            for entry in search_result:
                writer.writerow({'Company': entry['company'] if type(entry['company']) is not list else '',
                                    'Username': entry['sAMAccountName'],
                                    'Name': entry['cn'],
                                    'Title': entry['title'] if type(entry['title']) is not list else '',
                                    'Email': entry['userPrincipalName']if type(entry['userPrincipalName']) is not list else '',
                                    'Telephone': entry['telephoneNumber']if type(entry['telephoneNumber']) is not list else '',
                                    'Department': entry['department'] if type(entry['department']) is not list else '',
                                    'Manager': entry['manager']if type(entry['manager']) is not list else '',
                                    'Last Logon': entry['lastLogon'],
                                    'Last Logoff': entry['lastLogoff'],
                                    'Logon Count': entry['logonCount'],
                                    'Bad Password Count': entry['badPwdCount'],
                                    'Last Invalid Password': entry['badPasswordTime'],
                                    'Member': entry['memberof']if type(entry['memberof']) is not list else '',
                                    'Direct Reports':entry['directReports'] if type(entry['directReports']) is not list else '',
                                    'Created in':entry['whenCreated'] if type(entry['whenCreated']) is not list else '',
                                    'Last Change':entry['whenChanged'] if type(entry['whenChanged']) is not list else '',
                                    'Object Class':entry['objectClass'] if type(entry['objectClass']) is not list else '',
                                    'Account Expires': entry['accountExpires'] if type(entry['accountExpires']) is not list else ''
                                })
    else:
        fieldnames = ['Username',
                    'Name',
                    'Title',
                    'Email',
                    'Telephone',
                    'Department',
                    'Manager',
                    'Last Logon',
                    'Logon Count',
                    'Member',
                        ]

        writer = csv.DictWriter(csv_file,
                                fieldnames=fieldnames)
        writer.writeheader()
        if len(search_result) > 0:
            for entry in search_result:
                writer.writerow({'Username': entry['sAMAccountName'],
                                    'Name': entry['cn'],
                                    'Title': entry['title'] if type(entry['title']) is not list else '',
                                    'Email': entry['userPrincipalName']if type(entry['userPrincipalName']) is not list else '',
                                    'Telephone': entry['telephoneNumber']if type(entry['telephoneNumber']) is not list else '',
                                    'Department': entry['department'] if type(entry['department']) is not list else '',
                                    'Manager': entry['manager']if type(entry['manager']) is not list else '',
                                    'Last Logon': entry['lastLogon'],
                                    'Logon Count': entry['logonCount'],
                                    'Member': entry['memberof']if type(entry['memberof']) is not list else ''
                                })

        

    tk.messagebox.showinfo("LGR - Successfull", "Relatório Gerado")


style = ttk.Style()
style.configure('TButton', font = 
               ('calibri', 10, 'bold'), 
                ) 


var1 = tk.IntVar()
checkEntered = ttk.Checkbutton(root, text="LDAP over TLS", onvalue = 1, offvalue = 0, variable=var1, width=15)
checkEntered.grid(column=2,row=1, padx=8)

var2 = tk.IntVar()
checkEntered = ttk.Checkbutton(root, text="Auditor Mode", onvalue = 1, offvalue = 0, variable=var2, width=15)
checkEntered.grid(column=2,row=2, padx=8)

connect = ttk.Button(root, text = "Connect", width=25, style = 'TButton', command =click_me)
connect.grid(column= 1, row = 4,pady=3)

generate = ttk.Button(root, text = "Generate", width=25, style = 'TButton', command =generate_me)
generate.grid(column= 1, row =6,pady=3)

label3 = ttk.Label(root,text='version 1.0.4',font='Calibri 10 italic')
label3.grid(column=1,row=8)


root.mainloop()