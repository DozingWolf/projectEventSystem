from flask import current_app

class User():
    def __init__(self, userid, username, pcode, logintime) -> None:
        self.__userid = userid
        self.__username = username
        self.__permissioncode = pcode
        self.__logintime = logintime
        self.__is_login = False
    def getUserID(self):
        return self.__userid
    def getUserName(self):
        return self.__username
    def getUserPermissions(self):
        return self.__permissioncode
    def isLogin(self):
        self.__is_login = True
        return self.__is_login
    def isLogout(self):
        self.__is_login = False
        return self.__is_login
    def getLoginTime(self):
        return self.__logintime