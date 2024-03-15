CREATE TABLE IF NOT EXISTS core.listing (
    ListingID int PRIMARY KEY,
    UserID int NOT NULL REFERENCES core.kkuser(UserID),
    /*
    ListingName varchar NOT NULL,
    ListingDescription text,
    */
    AskingPrice numeric NOT NULL,
    CategoryTypeID int REFERENCES core.dim_categorytype(CategoryTypeID),
    CategoryID int,
    /*
    ImageDirectory varchar,
    */
    
    DateListed timestamp NOT NULL,
    /* DATETIME FKs */
    DateListedFK bigint NOT NULL,
    TimeListedFK varchar NOT NULL,
    
    ListingStatus char NOT NULL, /* O (open) , C (closed), S (sold) */

    DateChanged timestamp,
    /* DATETIME FKs */
    DateChangedFK bigint,
    TimeChangedFK varchar,

    SoldTo int REFERENCES core.kkuser(UserID),
    SoldPrice numeric,

    /* DERIVED FIELDS */
    TimeToClose numeric,
    DifferenceAskingSoldPrice numeric
);

CREATE INDEX IF NOT EXISTS ix_listing_userid ON core.listing (UserID);
CREATE INDEX IF NOT EXISTS ix_listing_categorytypeid ON core.listing (CategoryTypeID);
CREATE INDEX IF NOT EXISTS ix_listing_soldto ON core.listing (SoldTo);