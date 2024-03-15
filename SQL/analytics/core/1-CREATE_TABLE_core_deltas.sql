CREATE TABLE IF NOT EXISTS core.delta (
    DeltaID int PRIMARY KEY,
    UserID int DEFAULT 0,
    ListingID int DEFAULT 0,
    ReportID int DEFAULT 0,
    UserReportID int DEFAULT 0,
    ListingReportID int DEFAULT 0,
    ModReportID int DEFAULT 0
);

INSERT INTO core.delta VALUES (1);