CREATE TABLE IF NOT EXISTS datamart.modreport (
    ModReportID SERIAL PRIMARY KEY,
    ModReportDate timestamp,
    ModReportDateFK bigint,
    NumberOfNewReports int,
    NumberOfUnassignedReports int,
    NumberOfOpenReports int
)