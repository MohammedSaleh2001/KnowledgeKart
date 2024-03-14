CREATE TABLE IF NOT EXISTS listing (
    ListingID SERIAL PRIMARY KEY,
    UserID int NOT NULL REFERENCES kkuser(UserID),
    ListingName varchar NOT NULL,
    ListingDescription text,
    AskingPrice numeric NOT NULL,
    CategoryTypeID int REFERENCES categorytype(CategoryTypeID),
    CategoryID int,
    Condition varchar /* New, Very Good, Good, Used, Very Used */,
    ImageDirectory varchar,
    DateListed timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP(0),
    
    ListingStatus char NOT NULL DEFAULT 'O', /* O (open) , C (closed), S (sold) */
    DateChanged timestamp,
    SoldTo int REFERENCES kkuser(UserID),
    SoldPrice numeric
)