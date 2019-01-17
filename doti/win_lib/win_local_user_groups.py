import win32net
from .win_ad import getDomainUser, domainUserExists

def addUserToGroup(group, username, domain=None):
    if domainUserExists(username):
        win32net.NetGroupAddUser(domain, group, username)
