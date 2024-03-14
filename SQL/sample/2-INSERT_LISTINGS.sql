INSERT INTO listing (
    UserID,
    ListingName ,
    ListingDescription ,
    AskingPrice ,
    Condition 
) VALUES (
    3,
    'Calculus 1 Textbook',
    'Like new and hardly used',
    75,
    'New'
);

INSERT INTO listing (
    UserID,
    ListingName ,
    ListingDescription ,
    AskingPrice ,
    Condition 
) VALUES (
    4,
    'History 100 Textbook',
    'It is very old, but still better than the bookstore',
    10,
    'Very Used'
);

INSERT INTO listing (
    UserID,
    ListingName ,
    ListingDescription ,
    AskingPrice ,
    Condition ,
    ListingStatus  ,
    DateChanged ,
    SoldTo  ,
    SoldPrice
) VALUES (
    5,
    'ENGL 199 Textbook',
    'I hardly used it and I want it out of sight',
    10,
    'New',
    'S',
    '2024-04-15'::TIMESTAMP,
    3,
    10
);