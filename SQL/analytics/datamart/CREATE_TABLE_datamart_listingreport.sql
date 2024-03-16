CREATE TABLE IF NOT EXISTS datamart.listingreport (
    ListingReportDate timestamp PRIMARY KEY,
    ListingReportDateFK bigint,
    ListingReportTimeFK varchar,
    Category varchar,
    NumberOfNewListings int,
    NumberOfClosedListings int,
    NumberOfSoldListings int,
    AveragePercentSaleDifference numeric

)