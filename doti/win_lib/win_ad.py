from pyad import aduser

def getDomainUser(name):
    try:
        return aduser.ADUser.from_cn(name)
    except invalidResults:
        return None

def domainUserExists(username):
    try:
        aduser.ADUser.from_cn(username)
        return True
    except invalidResults:
        return False
