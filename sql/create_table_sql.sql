--项目事件记录工具
--人员表
create TABLE edm_test_schema.TMSTUSER
(userid int not null,--人员id
username varchar(10),--姓名
passwd varchar(200),--密码
createdate timestamp default now(),
createuserid int default 0,
modifydate timestamp default now(),
modifyuserid int default 0,
status int default 0,
isadmin varchar(2) not null default '00',
CONSTRAINT tmstuser_pk PRIMARY KEY (userid)
);
--部门表
create table edm_test_schema.TMSTDEPT
(deptid int not null,--部门id
deptname varchar(60),--部门名
createdate timestamp default now(),
createuserid int default 0,
modifydate timestamp default now(),
modifyuserid int default 0,
status int default 0,
CONSTRAINT tmstdept_pk PRIMARY KEY (deptid)
);
--项目概要表
create table edm_test_schema.TPRJPROJECT
(projectid int not null,--项目id
ownerid int,--项目所属货主部门编码
projectcode varchar(30),--项目编码
projectname varchar(200),--项目名
prjinitiatorid int,--项目发起人id
prjbrif varchar(800),--项目简介
prjcreationday timestamp default now(),--项目发起事件
createdate timestamp default now(),
createuserid int default 0,
modifydate timestamp default now(),
modifyuserid int default 0,
status int default 0,
CONSTRAINT tprjproject_pk PRIMARY KEY (projectid)
);
--项目事件表
create table edm_test_schema.TPRJEVENT
(projectid int not null,--项目id
eventid int not null,--事件id
eventtime timestamp default now(),--事件时间
eventcreationid int,--事件发起人id
eventstatus int,--事件状态id
eventmsg varchar(1000),--事件内容
createdate timestamp default now(),
createuserid int default 0,
modifydate timestamp default now(),
modifyuserid int default 0,
status int default 0,
CONSTRAINT tprjevent_pk PRIMARY KEY (eventid)
);
--项目成员关系表
create table edm_test_schema.TRLTPRJMEMBER
(projectid int not null,--项目id
userid int not null default 0,--用户id
memberstatus int default 0,--成员状态
createdate timestamp default now(),
createuserid int default 0,
modifydate timestamp default now(),
modifyuserid int default 0,
status int default 0,
CONSTRAINT trltprjmember_pk PRIMARY KEY (projectid, userid)
);
