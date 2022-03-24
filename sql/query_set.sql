--查询项目所属参与人
select
p.projectcode,p.prjbrif,u.username
from edm_test_schema.tprjproject p
inner join edm_test_schema.trltprjmember m on p.projectid = m.projectid and m.status = 0
inner join edm_test_schema.tmstuser u on m.userid = u.userid and u.status = 0
where 1=1
and p.status = 0
--查询项目对应的事件记录
select
p.projectcode,p.projectname,e.eventtime,e.eventmsg,u.username as recorder,
d.deptname as prjowner
from edm_test_schema.tprjproject p 
inner join edm_test_schema.tprjevent e on p.projectid = e.projectid and e.status = 0
inner join edm_test_schema.tmstuser u on p.prjinitiatorid = u.userid
inner join edm_test_schema.tmstdept d on p.ownerid = d.deptid
where 1=1
and p.status = 0
--查询项目成员及部门
select 
p.projectcode,p.projectname,u.username,m.memberstatus,d.deptname
from edm_test_schema.trltprjmember m 
inner join edm_test_schema.tmstuser u on m.userid = u.userid
inner join edm_test_schema.tprjproject p on p.projectid = m.projectid
inner join edm_test_schema.tmstdept d on p.ownerid = d.deptid
where 1=1
and p.status = 0