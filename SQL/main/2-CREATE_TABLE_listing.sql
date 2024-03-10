CREATE TABLE IF NOT EXISTS listing (
    ListingID SERIAL PRIMARY KEY,
    UserID int NOT NULL REFERENCES kkuser(UserID),
    ListingName varchar NOT NULL,
    ListingDescription text,
    AskingPrice numeric NOT NULL,
    CategoryTypeID int REFERENCES categorytype(CategoryTypeID),
    CategoryID int,
    ImageDirectory varchar,
    DateListed timestamp NOT NULL,
    
    ListingStatus char NOT NULL, /* O (open) , C (closed), S (sold) */
    DateChanged timestamp,
    SoldTo int REFERENCES kkuser(UserID),
    SoldPrice numeric
)