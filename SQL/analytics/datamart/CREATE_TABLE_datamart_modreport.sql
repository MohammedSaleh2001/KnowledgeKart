CREATE TABLE IF NOT EXISTS datamart.modreport (
    ModReportDate timestamp PRIMARY KEY,
    ModReportDateFK bigint,
    ModReportTimeFK varchar,
    NumberOfNewReports int,
    NumberOfUnassignedReports int,
    NumberOfOpenReports int
)