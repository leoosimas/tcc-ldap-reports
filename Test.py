import ldap3
from os import path
from getpass import getpass
import sys
import pyad



host='192.168.1.19'
host = ldap3.Server(host)
user='administrator@tcclab.com'
passwd = '1234Qwer'

connection = ldap3.Connection(host, user=user, password=passwd)
connection.bind()


