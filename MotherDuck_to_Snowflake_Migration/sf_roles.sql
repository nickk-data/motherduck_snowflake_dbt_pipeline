use role securityadmin;

create role if not exists engineering_role;
create role if not exists analyst_role;

grant all privileges on database data_jobs to role engineering_role;
grant all privileges on schemas in database data_jobs to role engineering_role;
grant all privileges on tables in database data_jobs to role engineering_role;


grant usage on databsae data_jobs to role analyst_role;
grant usage on all schemas in database data_jobs to role analyst_role;
grant usage on all tables in database data_jobs to role analyst_role;

grant role engineering_role to role sysadmin;
grant role analyst_role to role sysadmin;

grant role engineering_role to user user1
/* dummied for github purposes */