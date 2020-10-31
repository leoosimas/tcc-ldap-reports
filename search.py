from ldap3 import Server, Connection, SUBTREE
total_entries = 0
server = Server('192.168.1.19')
c = Connection(server, user='administrator@tcclab.com', password='1234Qwer')

filter=u'(&(objectClass=user))'
attributes = ''
basedn='CN=Users,CN=Builtin'

entry_list = c.extend.standard.paged_search(search_base = 'o=test',
                                            search_filter = '(objectClass=inetOrgPerson)',
                                            search_scope = SUBTREE,
                                            attributes = ['cn', 'givenName'],
                                            paged_size = 5,
                                            generator=False)
for entry in entry_list:
    print (entry['attributes'])
total_entries = len(entry_list)
print('Total entries retrieved:', total_entries)