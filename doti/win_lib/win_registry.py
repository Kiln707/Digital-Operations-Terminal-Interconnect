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
        if not self.__class__.validRoot(root):
            raise ValueError()
        self._root=root
        self._path=path
        self._properties={}
        self._importKey()

    def _importKey(self):
        if self.exists():
            with winreg.OpenKey(self._root, self._path) as k:
                keyinfo=winreg.QueryInfoKey(k)
                for i in range(0, keyinfo[1]):
                    value = winreg.EnumValue(k, i)
                    self._properties[value[0]] = (value[1], value[2])

    def __getattr__(self, value):
        if value not in self._properties:
            raise AttributeError()
        return self._properties[value]

    def __setattr__(self, name, value):
        pass

    def getProperties(self):
        return self._properties.keys()

    def exists(self):
        try:
            with winreg.OpenKey(self._root, self._path):
                pass
            return True
        except:
            return False

    @classmethod
    def validRoot(cls, key):
        return key in cls.__dict__


if __name__ == '__main__':
    r = RegistryKey('HKEY_LOCAL_MACHINE', r'SOFTWARE\7-Zip')
    print(RegistryProperty.__dict__)
