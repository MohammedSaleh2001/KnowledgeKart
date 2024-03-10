CREATE TABLE IF NOT EXISTS core.kkuser (
    UserID SERIAL PRIMARY KEY,
    
    Email varchar UNIQUE, 
    /*
    HashPass varchar NOT NULL,
    Salt varchar NOT NULL,
    */
    FirstName varchar NOT NULL,
    DateJoined timestamp NOT NULL,

    /* DATETIME FKs */
    DateJoinedFK bigint NOT NULL,
    TimeJoinedFK varchar NOT NULL,

    UserRole char NOT NULL,
    Verified boolean NOT NULL,
    Blacklist boolean NOT NULL,
    /*
    BlacklistedUntil timestamp,
    */
    Politeness numeric NOT NULL,
    Honesty numeric NOT NULL,
    Quickness numeric NOT NULL,
    NumReviews int NOT NULL,

    /* DERIVED FIELDS */
    NumberOfChats int NOT NULL,
    NumberOfListings int NOT NULL,
    NumberOfSoldListings int NOT NULL,
    NumberOfClosedListings int NOT NULL,
    NumberOfBoughtListings int NOT NULL,
    NumberOfReports int NOT NULL,
    AvgUserRating numeric NOT NULL
)