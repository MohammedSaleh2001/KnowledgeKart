CREATE TABLE IF NOT EXISTS datamart.userreport (
    UserReportDate timestamp PRIMARY KEY,
    UserReportDateFK bigint,
    UserReportTimeFK varchar,
    NumUnverifiedUsers int,
    NumVerifiedUsers int,
    NumBlacklistedUsers int,
    NumTotalUsers int,
    AvgUserRating numeric
)