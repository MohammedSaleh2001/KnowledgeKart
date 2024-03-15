CREATE TABLE IF NOT EXISTS datamart.modreport (
    ModReportID SERIAL PRIMARY KEY,
    ModReportDate timestamp,
    ModReportDateFK bigint,
    ModReportTimeFK varchar,
    NumberOfNewReports int,
    NumberOfUnassignedReports int,
    NumberOfOpenReports int
)