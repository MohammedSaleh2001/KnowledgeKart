CREATE TABLE IF NOT EXISTS datamart.listingreport (
    ListingReportID SERIAL PRIMARY KEY,
    ListingReportDate timestamp,
    ListingReportDateFK bigint,
    Category varchar,
    NumberOfNewListings int,
    NumberOfClosedListings int,
    NumberOfSoldListings int,
    AveragePercentSaleDifference numeric

)