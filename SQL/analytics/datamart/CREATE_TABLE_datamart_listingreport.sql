CREATE TABLE IF NOT EXISTS datamart.listingreport (
    ListingReportDate timestamp PRIMARY KEY,
    ListingReportDateFK bigint,
    ListingReportTimeFK varchar,
    NumOpenListings int,
    NumClosedListings int,
    NumSoldListings int

)