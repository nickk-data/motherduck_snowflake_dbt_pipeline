use role sysadmin;
use database data_jobs;
use schema motherduck_migration;

select * from motherduck_migration.job_postings_fact at(offset => -600);

drop table motherduck_migration.job_postings_fact;

undrop table motherduck_migration.job_postings_fact;