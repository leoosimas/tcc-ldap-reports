import tkinter as tk
from tkinter import filedialog, Text
from tkinter import ttk
import os
import ldap3

root = tk.Tk()

root.title("LDAP REPORT GENERATOR")
root.minsize(400,400)





label = ttk.Label(root,text='Server')
label.grid(column=0,row=0)

label1 = ttk.Label(root,text='User')
label1.grid(column=0,row=1)

label2 = ttk.Label(root,text='Password')
label2.grid(column=0,row=2)


serverEntered = ttk.Entry(root, width = 30)
serverEntered.grid(column=1,row=0)


userEntered = ttk.Entry(root, width = 30)
userEntered.grid(column=1,row=1)


passwdEntered = ttk.Entry(root,show = "*", width = 30)
passwdEntered.grid(column=1,row=2)

def ClickMe():
    
    conn = ldap3.Connection(serverEntered.get(), userEntered.get(), passwdEntered.get())

    conn.bind()
    
    conn.search('cn=Users,dc=tcclab,dc=com', '(&(objectclass=person))', attributes=ldap3.ALL_ATTRIBUTES)

    search_result = conn.entries

    print(search_result)

    return search_result


connect = ttk.Button(root, text = "Connect", width=15,command = ClickMe)
connect.grid(column= 3, row = 1)

generate = ttk.Button(root, text = "Generate Report", width=15)
generate.grid(column=3, row=2)


root.mainloop()