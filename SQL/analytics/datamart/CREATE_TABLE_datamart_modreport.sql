CREATE TABLE IF NOT EXISTS datamart.modreport (
    ModReportDate timestamp PRIMARY KEY,
    ModReportDateFK bigint,
    ModReportTimeFK varchar,
    NumOpenReports int,
    NumUnassignedReports int,
    NumClosedReports int,
    NumTotalReports int
)