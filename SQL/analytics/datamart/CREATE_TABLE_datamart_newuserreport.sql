CREATE TABLE IF NOT EXISTS datamart.newuserreport (
    NewUserReportDate timestamp PRIMARY KEY,
    NewUserReportDateFK bigint,
    NewUserReportTimeFK varchar,
    NumNewUsers int
)