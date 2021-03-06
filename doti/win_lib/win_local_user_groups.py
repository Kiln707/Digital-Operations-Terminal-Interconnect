import win32net, json
from win_ad import getDomainUser, domainUserExists

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

def getUserSID(username, domain=None):
    return win32net.NetUserGetInfo('solano.cc.ca.us', 'sswanson', 4)['user_sid']

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

if __name__ == '__main__':
    #addUserToLocalGroup('Administrators', 'testing')
    removeUserFromLocalGroup('Administrators', 'gtom', 'NTNET')

    print(win32net.NetLocalGroupGetMembers(None, 'Administrators', 2))
    #win32net.NetLocalGroupDelMembers(None, 'Administrators', [json.dumps({'domainandname':'NTNET\\gtom'})])
