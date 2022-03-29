from werkzeug.security import check_password_hash, generate_password_hash
from model import db

class User(db.Model):
    __tablename__ = 'TMSTUSER'
    userid = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.VARCHAR(10))
    passwd = db.Column(db.VARCHAR(200))
    createuserid = db.Column(db.Integer)
    modifyuserid = db.Column(db.Integer)
    status = db.Column(db.Integer)
    createdate = db.Column(db.TIMESTAMP)
    modifydate = db.Column(db.TIMESTAMP)
    isadmin = db.Column(db.VARCHAR(2))
    is_anonymous = False

    def __init__(self, *args, **kw) -> None:
        super(User,self).__init__(*args, **kw)
        self._authenticated = False
    
    def set_password(self, pw):
        self.password = generate_password_hash(pw)

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, pw):
        checked = check_password_hash(self.password, pw)
        self._authenticated = checked
        return self._authenticated

    def get_id(self):
        return self.userid

class Dept(db.Model):
    __tablename__ = 'TMSTDEPT'
    deptid = db.Column(db.Integer,primary_key=True)
    deptname = db.Column(db.VARCHAR(60))
    createdate = db.Column(db.TIMESTAMP)
    createuserid = db.Column(db.Interger)
    modifydate = db.Column(db.TIMESTAMP)
    modifyuserid = db.Column(db.Interger)
    status = db.Column(db.Integer)

    def __init__(self, *args, **kw) -> None:
        super(Dept,self).__init__(*args, **kw)

class Project(db.Model):
    __tablename__ = 'TPRJPROJECT'
    projectid = db.Column(db.Integer,primary_key=True)
    ownerid = db.Column(db.Integer) # 项目所属货主部门编码
    projectcode = db.Column(db.VARCHAR(30)) # 项目编码
    projectname = db.Column(db.VARCHAR(200)) # 项目名
    prjinitiatorid = db.Column(db.Integer) # 项目发起人id
    prjbrif = db.Column(db.VARCHAR(800)) # 项目简介
    prjcreationday = db.Column(db.TIMESTAMP) # 项目发起事件
    createdate = db.Column(db.TIMESTAMP)
    createuserid = db.Column(db.Interger)
    modifydate = db.Column(db.TIMESTAMP)
    modifyuserid = db.Column(db.Interger)
    status = db.Column(db.Integer)

    def __init__(self, *args, **kw) -> None:
        super(Project,self).__init__(*args, **kw)

class Event(db.Model):
    __tablename__ = 'TPRJEVENT'
    projectid = db.Column(db.Integer) # 项目id
    eventid = db.Column(db.Integer,primary_key=True) # 事件id
    eventtime = db.Column(db.TIMESTAMP) # 事件时间
    eventcreationid = db.Column(db.Integer) # 事件发起人id
    eventstatus = db.Column(db.Integer) # 事件状态id
    eventmsg = db.Column(db.VARCHAR(1000)) # 事件内容
    createdate = db.Column(db.TIMESTAMP)
    createuserid = db.Column(db.Interger)
    modifydate = db.Column(db.TIMESTAMP)
    modifyuserid = db.Column(db.Interger)
    status = db.Column(db.Integer)

    def __init__(self, *args, **kw) -> None:
        super(Event,self).__init__(*args, **kw)