--项目事件记录工具

-- edm_test_schema.tmstdept definition

-- Drop table

-- DROP TABLE edm_test_schema.tmstdept;

--部门表
CREATE TABLE edm_test_schema.tmstdept (
	deptid int4 NOT NULL,
	deptname varchar(60) NULL,
	createdate timestamp NULL DEFAULT now(),
	createuserid int4 NULL DEFAULT 0,
	modifydate timestamp NULL DEFAULT now(),
	modifyuserid int4 NULL DEFAULT 0,
	status int4 NULL DEFAULT 0,
	CONSTRAINT tmstdept_pk PRIMARY KEY (deptid),
	CONSTRAINT unikey_tmstdept_deptname UNIQUE (deptname)
);


-- edm_test_schema.tmstpermission definition

-- Drop table

-- DROP TABLE edm_test_schema.tmstpermission;

--权限明细表
CREATE TABLE edm_test_schema.tmstpermission (
	permissionid int4 NOT NULL,
	permissionname varchar(30) NOT NULL,
	urlitem varchar(100) NOT NULL,
	createdate timestamp NULL DEFAULT now(),
	createuserid int4 NULL DEFAULT 0,
	modifydate timestamp NULL DEFAULT now(),
	modifyuserid int4 NULL DEFAULT 0,
	status int4 NULL DEFAULT 0,
	CONSTRAINT tmstpermission_pk PRIMARY KEY (permissionid),
	CONSTRAINT unikey_tmstpermission_pid_url UNIQUE (permissionid, urlitem)
);


-- edm_test_schema.tmstuser definition

-- Drop table

-- DROP TABLE edm_test_schema.tmstuser;
--人员表
CREATE TABLE edm_test_schema.tmstuser (
	userid int4 NOT NULL,
	username varchar(10) NULL,
	passwd varchar(200) NULL,
	createdate timestamp NULL DEFAULT now(),
	createuserid int4 NULL DEFAULT 0,
	modifydate timestamp NULL DEFAULT now(),
	modifyuserid int4 NULL DEFAULT 0,
	status int4 NULL DEFAULT 0,
	isadmin varchar(2) NOT NULL DEFAULT '00'::character varying,
	CONSTRAINT tmstuser_pk PRIMARY KEY (userid),
	CONSTRAINT unikey_tmstuser_id_uname UNIQUE (username, userid)
);


-- edm_test_schema.tmstuserpermission definition

-- Drop table

-- DROP TABLE edm_test_schema.tmstuserpermission;

--权限主表
CREATE TABLE edm_test_schema.tmstuserpermission (
	userid int4 NOT NULL,
	permissionid int4 NOT NULL,
	permissionmemo varchar(100) NULL,
	createdate timestamp NULL DEFAULT now(),
	createuserid int4 NULL DEFAULT 0,
	modifydate timestamp NULL DEFAULT now(),
	modifyuserid int4 NULL DEFAULT 0,
	status int4 NULL DEFAULT 0,
	CONSTRAINT tmstuserpermission_pk PRIMARY KEY (userid, permissionid)
);
COMMENT ON TABLE edm_test_schema.tmstuserpermission IS '权限组头表';
COMMENT ON COLUMN edm_test_schema.tmstuserpermission.userid IS '权限用户ID';
COMMENT ON COLUMN edm_test_schema.tmstuserpermission.permissionid IS '权限组ID';
COMMENT ON COLUMN edm_test_schema.tmstuserpermission.permissionmemo IS '权限组添加说明';

-- edm_test_schema.tprjevent definition

-- Drop table

-- DROP TABLE edm_test_schema.tprjevent;

--项目事件表
CREATE TABLE edm_test_schema.tprjevent (
	projectid int4 NOT NULL,
	eventid int4 NOT NULL,
	eventtime timestamp NULL DEFAULT now(),
	eventcreationid int4 NULL,
	eventstatus int4 NULL,
	eventmsg varchar(1000) NULL,
	createdate timestamp NULL DEFAULT now(),
	createuserid int4 NULL DEFAULT 0,
	modifydate timestamp NULL DEFAULT now(),
	modifyuserid int4 NULL DEFAULT 0,
	status int4 NULL DEFAULT 0,
	CONSTRAINT tprjevent_pk PRIMARY KEY (eventid)
);


-- edm_test_schema.tprjproject definition

-- Drop table

-- DROP TABLE edm_test_schema.tprjproject;

--项目概要表
CREATE TABLE edm_test_schema.tprjproject (
	projectid int4 NOT NULL,
	ownerid int4 NULL,
	projectcode varchar(30) NULL,
	projectname varchar(200) NULL,
	prjinitiatorid int4 NULL,
	prjbrif varchar(800) NULL,
	prjcreationday timestamp NULL DEFAULT now(),
	createdate timestamp NULL DEFAULT now(),
	createuserid int4 NULL DEFAULT 0,
	modifydate timestamp NULL DEFAULT now(),
	modifyuserid int4 NULL DEFAULT 0,
	status int4 NULL DEFAULT 0,
	CONSTRAINT tprjproject_pk PRIMARY KEY (projectid)
);


-- edm_test_schema.trltprjmember definition

-- Drop table

-- DROP TABLE edm_test_schema.trltprjmember;

--项目成员关系表
CREATE TABLE edm_test_schema.trltprjmember (
	projectid int4 NOT NULL,
	userid int4 NOT NULL DEFAULT 0,
	memberstatus int4 NULL DEFAULT 0,
	createdate timestamp NULL DEFAULT now(),
	createuserid int4 NULL DEFAULT 0,
	modifydate timestamp NULL DEFAULT now(),
	modifyuserid int4 NULL DEFAULT 0,
	status int4 NULL DEFAULT 0,
	CONSTRAINT trltprjmember_pk PRIMARY KEY (projectid, userid)
);

