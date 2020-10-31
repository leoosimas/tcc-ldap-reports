import tkinter as tk
from tkinter import filedialog, Text
from tkinter import ttk
import os

root = tk.Tk()

root.title("LDAP REPORT GENERATOR")
root.minsize(400,400)





label = ttk.Label(root,text='Server')
label.grid(column=0,row=0)

label1 = ttk.Label(root,text='User')
label1.grid(column=0,row=1)

label2 = ttk.Label(root,text='Password')
label2.grid(column=0,row=2)

server = tk.StringVar()
serverEntered = ttk.Entry(root, width = 30, textvariable = server)
serverEntered.grid(column=1,row=0)

user = tk.StringVar()
userEntered = ttk.Entry(root, width = 30, textvariable = user)
userEntered.grid(column=1,row=1)

passwd = tk.StringVar()
passwdEntered = ttk.Entry(root,show = "*", width = 30, textvariable = passwd)
passwdEntered.grid(column=1,row=2)


connect = ttk.Button(root, text = "Connect", width=15)
connect.grid(column= 3, row = 2)


root.mainloop()