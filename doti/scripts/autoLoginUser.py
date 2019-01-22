import argparse, socket

try:
    import _winreg as _winreg
except ImportError:
    import winreg

###############################################
#   Windows Registry Handler
#
#   Author: Steven Swanson
#----------------------------------------------
#   Allows for lookup and editing of Windows Registry
#   Features:
#       - Check if key and/or property exists
#       - Get key, property, values
#       - Compare key, property, values
#       - Create Key, property, values
#       - Delete Key, property, values
################################################

class RegistryProperty():
    NONE=winreg.REG_NONE
    SZ=winreg.REG_SZ
    EXPAND_SZ=winreg.REG_EXPAND_SZ
    BINARY=winreg.REG_BINARY
    DWORD32=winreg.REG_DWORD # 4
    DWORD32LE=winreg.REG_DWORD_LITTLE_ENDIAN # 4
    DWORD32BE=winreg.REG_DWORD_BIG_ENDIAN
    LINK=winreg.REG_LINK
    MULTI_SZ=winreg.REG_MULTI_SZ
    RESOURCE_LIST=winreg.REG_RESOURCE_LIST
    FULL_RESOURCE_DESCRIPTOR=winreg.REG_FULL_RESOURCE_DESCRIPTOR
    RESOURCE_REQUIREMENTS_LIST=winreg.REG_RESOURCE_REQUIREMENTS_LIST
    QWORD=winreg.REG_QWORD # 11
    QWORD_LE=winreg.REG_QWORD_LITTLE_ENDIAN # 11

    def __init__(self, name, value, propertyType):
        self.name = name
        self.value=value
        if type(propertyType) is int:
            self.type=self._intToPropertyType(propertyType)
        elif self._validType(propertyType):
            self.type=propertyType
        else:
            raise ValueError()

    def getType(self):
        return self.__class__.__dict__[self.type]

    def __str__(self):
        return "<RegistryProperty %s type:%s, value:%s>"%(self.value, self.type, self.value)

    @classmethod
    def _validType(cls, propertyType):
        if propertyType.startswith('_'):
            raise ValueError()
        return propertyType in cls.__dict__

    @classmethod
    def _intToPropertyType(cls, integer):
        if integer > 11:
            raise ValueError()
        for key, value in cls.__dict__.items():
            if value == integer:
                return key


class RegistryKey():
    HKEY_CLASSES_ROOT=winreg.HKEY_CLASSES_ROOT
    HKEY_CURRENT_USER=winreg.HKEY_CURRENT_USER
    HKEY_LOCAL_MACHINE=winreg.HKEY_LOCAL_MACHINE
    HKEY_USERS=winreg.HKEY_USERS
    HKEY_PERFORMANCE_DATA=winreg.HKEY_PERFORMANCE_DATA
    HKEY_CURRENT_CONFIG=winreg.HKEY_CURRENT_CONFIG
    HKCR=winreg.HKEY_CLASSES_ROOT
    HKCU=winreg.HKEY_CURRENT_USER
    HKLM=winreg.HKEY_LOCAL_MACHINE
    HKU=winreg.HKEY_USERS
    HKPD=winreg.HKEY_PERFORMANCE_DATA
    HKCC=winreg.HKEY_CURRENT_CONFIG

    def __init__(self, root, path):
        if not self.validRoot(root):
            raise ValueError()
        if type(root) is str:
            self._root=self.__class__.__dict__[root]
        else:
            self._root=root
        self._path=path
        self._subkeys=[]
        self._properties=[]
        self._importKey()

    def _importKey(self):
        if self.exists():
            with self._openkey() as k:
                keyinfo=winreg.QueryInfoKey(k)
                for value in self._getKeyProperties(k):
                    self._properties.append(value[0])
                    setattr(self, value[0], RegistryProperty(value[0], value[1], value[2]))
                for i in range(0, keyinfo[0]):
                    value = winreg.EnumKey(k, i)
                    self._subkeys.append(value)

    def save(self):
        if self.exists():
            with self._openkey(access=winreg.KEY_ALL_ACCESS) as k:
                self._saveData(k)
        else:
            with winreg.CreateKeyEx(self._root, self._path, 0, access=winreg.KEY_SET_VALUE) as k:
                self._saveData(k)

    def _saveData(self, handle):
        current_data=[]
        with self._openkey() as k:
            current_data =self._getKeyProperties(k)
        for val in current_data:
            if val[0] not in self._properties:
                winreg.DeleteValue(handle, val[0])
        for prop in self._properties:
            data = getattr(self, prop)
            winreg.SetValueEx(handle, data.name, 0, data.getType(), data.value)

    def _openkey(self, access=winreg.KEY_READ):
        return winreg.OpenKey(self._root, self._path, access=access)

    def newProperty(self, prop):
        if not isinstance(prop, RegistryProperty):
            raise ValueError()
        setattr(self, prop.name, prop)
        self._properties.append(prop.name)

    def deleteProperty(self, prop):
        if getattr(self, prop):
            delattr(self, prop)
        self._properties.remove(prop)

    def setProperty(self, prop, value):
        setattr(self, prop, value)

    def hasProperty(self, prop):
        return hasattr(self, prop)

    def getProperty(self, property):
        return getattr(self, prop)

    def getProperties(self):
        return list(self._properties)

    def _getKeyProperties(self, handle):
        props=[]
        keyinfo=winreg.QueryInfoKey(handle)
        for i in range(0, keyinfo[1]):
            value = winreg.EnumValue(handle, i)
            props.append(value)
        return props

    def contains(self, property):
        if isinstance(property, RegistryKey):
            pass    #TODO: IMPLEMENT
        elif isinstance(property, RegistryProperty):
            if property.name in self._properties:
                return True
            return False
        else:
            raise AttributeError()

    def getSubKeys(self):
        return list(self._subkeys)

    def getSubKey(self, name):
        if name not in self._subkeys:
            raise AttributeError()
        return RegistryKey(self._root, self._path+"\\%s"%name)

    def delete(self):
        winreg.DeleteKey(self._root, self._path)

    def exists(self):
        try:
            with winreg.OpenKey(self._root, self._path):
                pass
            return True
        except:
            return False

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.save()

    @classmethod
    def validRoot(cls, key):
        return key in cls.__dict__ or key in cls.__dict__.values()

##############################################################################################
#
#
#
##############################################################################################
def setArgs(parser):
    parser.add_argument('--domain', action='store')
    parser.add_argument('--user', action='store')
    parser.add_argument('--password', action='store')

parser = argparse.ArgumentParser(description="Set computer to Automatically Login as User")
sub = parser.add_subparsers(dest='action', help = 'Command Help')
on = sub.add_parser('on', help='Turn on autologin')
off = sub.add_parser('off', help='Turn off autologin')
setArgs(on)
setArgs(off)
args = parser.parse_args()

data=[]

if args.action == 'on':
    data.append(RegistryProperty('AutoAdminLogon', '1', 'SZ'))
    data.append(RegistryProperty('ForceAutoLogin', '1', 'SZ'))
else:
    data.append(RegistryProperty('AutoAdminLogon', '0', 'SZ'))
    data.append(RegistryProperty('ForceAutoLogin', '0', 'SZ'))

if args.user:
    data.append(RegistryProperty('DefaultUserName', args.user, 'SZ'))
    if args.domain:
        data.append(RegistryProperty('DefaultDomainName', args.domain, 'SZ'))
    if args.password:
        data.append(RegistryProperty('DefaultPassword', args.password, 'SZ'))
    else:
        data.append(RegistryProperty('DefaultPassword', '', 'SZ'))
else:
    if args.domain:
        raise ValueError("--user must be provided when using --domain")

with RegistryKey('HKLM', 'SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon') as regkey:
    for prop in data:
        if regkey.contains(prop):
            regkey.setProperty(prop.name, prop)
        else:
            regkey.newProperty(prop)
