INSERT INTO listing (
    UserID,
    ListingName ,
    ListingDescription ,
    AskingPrice ,
    Condition,
    DateListed
) VALUES (
    4,
    'Calculus 1 Textbook',
    'Like new and hardly used',
    75,
    'New',
    '2024-03-12'::TIMESTAMP
);

INSERT INTO listing (
    UserID,
    ListingName ,
    ListingDescription ,
    AskingPrice ,
    Condition ,
    DateListed 
) VALUES (
    5,
    'History 100 Textbook',
    'It is very old, but still better than the bookstore',
    10,
    'Very Used',
    '2024-03-12'::TIMESTAMP
);

INSERT INTO listing (
    UserID,
    ListingName ,
    ListingDescription ,
    AskingPrice ,
    Condition ,
    DateListed,
    ListingStatus  ,
    DateChanged ,
    SoldTo  ,
    SoldPrice
) VALUES (
    6,
    'ENGL 199 Textbook',
    'I hardly used it and I want it out of sight',
    10,
    'New',
    '2024-03-12'::TIMESTAMP,
    'S',
    '2024-03-13 12:00:00'::TIMESTAMP,
    4,
    10
);

INSERT INTO listing (
    UserID,
    ListingName ,
    ListingDescription ,
    AskingPrice ,
    Condition
) VALUES (
    5,
    'ENG PHYS 130 Textbook',
    'Tough course, so I took it out on the book a few times.',
    5,
    'Very Used'
);