import argparse

import win32net, json

def userExists(username, domain=None):
    try:
        win32net.NetUserGetInfo(domain, username, 0)
        return True
    except:
        return False

def getDomainUser(username, domain=None, info_level=0):
    if userExists(username, domain):
        return win32net.NetUserGetInfo(domain, username, info_level)
    else:
        return None

def localGroupExists(groupname):
    try:
        win32net.NetLocalGroupGetInfo(None, groupname, 0)
        return True
    except:
        return False

def addUserToLocalGroup(group, username, domain=None):
    if localGroupExists(group):
        if domain and userExists(username, domain):
            win32net.NetLocalGroupAddMembers(None, group, 3, [{'domainandname':domain+'\\'+username}])
        elif userExists(username):
            win32net.NetLocalGroupAddMembers(None, group, 3, [{'domainandname':username}])

def removeUserFromLocalGroup(group, username, domain=None):
    if localGroupExists(group):
        if domain and userExists(username, domain):
            win32net.NetLocalGroupDelMembers(None, group, [r'%s\\%s'%(domain,username)])
        elif userExists(username):
            win32net.NetLocalGroupDelMembers(None, group, [r"%s"%username])



parser = argparse.ArgumentParser(description="Add users to Administrators Local Group.")
parser.add_argument('--domain', action='store')
parser.add_argument('users', nargs=argparse.REMAINDER)

args = parser.parse_args()
for user in args.users:
    addUserToLocalGroup('Administrators', user, args.domain)
