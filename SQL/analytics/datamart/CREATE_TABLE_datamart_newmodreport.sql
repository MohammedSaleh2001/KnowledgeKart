CREATE TABLE IF NOT EXISTS datamart.newmodreport (
    NewModReportDate timestamp PRIMARY KEY,
    NewModReportDateFK bigint,
    NewModReportTimeFK varchar,
    NumNewReports int,
    NumClosedReports int,
    AverageTimeToClose numeric
)