use role accountadmin;

alter warehouse compute_wh 
set 
    auto_suspend = 60
    auto_resume = true;

create or replace resource monitor credit_guard
with credit_quota = 10
frequency = monthly
start_time = immediately
triggers
    on 80 percent do notify
    on 100 percent do suspend
    on 110 percent do suspend_immediate;

alter warehouse compute_wh set resource_monitor = credit_guard;

