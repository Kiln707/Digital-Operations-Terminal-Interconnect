from pyad import *

from pyad import aduser, adbase, adquery
from pyad.pyadexceptions import invalidResults

def init_pyad(fqdn, username, password):
    adbase.set_defaults(ldap_server=fqdn, username=username, password=password, user=aduser.ADUser.from_cn(username))

def QueryAD(attributes=[], where='', OU=''):
    q = adquery.ADQuery()
    q.execute_query(attributes=attributes, where_clause=where, base_dn=OU)
    return q.get_results()

def getDomainUser(name, OU):
    attributes=['distinguishedName']
    where="sAMAccountName = '%s'"%name
    return aduser.ADUser.from_dn(list(QueryAD(attributes, where, OU))[0]['distinguishedName'])

def domainUserExists(username):
    q = adquery.ADQuery()
    q.execute_query(attributes=['distinguishedName'],
        where_clause="sAMAccountName = '%s'"%username,
        base_dn = "OU=Accounts, DC=solano, DC=cc, DC=ca, DC=us")
    return len(list(q.get_results())) == 1


if __name__ == '__main__':
    q = adquery.ADQuery()
    q.execute_query(attributes=['distinguishedName'],
        where_clause="sAMAccountName = 'sswanson'",
        base_dn = "DC=solano, DC=cc, DC=ca, DC=us")
    for r in q.get_results():
        print(r)
