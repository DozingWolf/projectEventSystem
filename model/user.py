from flask import current_app

class User():
    def __init__(self, userid, username, pcode) -> None:
        self.userid = userid
        self.username = username
        self.permissioncode = pcode
    def getUserID(self):
        return self.userid
    def getUserName(self):
        return self.username
    def getUserPermissions(self):
        return self.permissioncode