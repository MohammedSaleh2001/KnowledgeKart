CREATE TABLE IF NOT EXISTS datamart.newlistingreport (
    NewListingReportDate timestamp,
    NewListingReportDateFK bigint,
    NewListingReportTimeFK varchar,
    Category varchar,
    Condition varchar,
    NumNewListings int,
    NumClosedListings int,
    NumSoldListings int,
    AverageCloseTime numeric,
    AverageSellTime numeric,
    AveragePriceSaleDifference numeric,
    AveragePercentSaleDifference numeric,
    PRIMARY KEY(NewListingReportDate, Category, Condition)
)