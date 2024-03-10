CREATE TABLE IF NOT EXISTS datamart.userreport (
    UserReportID SERIAL PRIMARY KEY,
    UserReportDate timestamp,
    UserReportDateFK bigint,
    NumNewUsers int,
    NumUnverifiedUsers int,
    NumVerifiedUsers int,
    NumBlacklistedUsers int,
    AvgUserRating numeric
)