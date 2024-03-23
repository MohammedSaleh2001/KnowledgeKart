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

/* Sale 1 - Alice (6) to Joe (4) */

INSERT INTO listing (
    UserID,
    ListingName ,
    ListingDescription ,
    AskingPrice ,
    CategoryTypeID,
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
    2,
    'New',
    '2024-03-12'::TIMESTAMP,
    'S',
    '2024-03-13 12:00:00'::TIMESTAMP,
    4,
    10
);

/* Sale 2 - Bob (5) to Tim (7) */

INSERT INTO listing (
    UserID,
    ListingName ,
    ListingDescription ,
    AskingPrice ,
    CategoryTypeID,
    Condition ,
    DateListed,
    ListingStatus  ,
    DateChanged ,
    SoldTo  ,
    SoldPrice
) VALUES (
    5,
    'History 100 Textbook',
    'It is very old, but still better than the bookstore',
    10,
    2,
    'Very Used',
    '2024-03-12'::TIMESTAMP,
    'S',
    '2024-03-14 16:00:00'::TIMESTAMP,
    7,
    5
);

/* Sale 3 - Bob (5) to Mark (8) */

INSERT INTO listing (
    UserID,
    ListingName ,
    ListingDescription ,
    AskingPrice ,
    CategoryTypeID,
    Condition ,
    DateListed,
    ListingStatus  ,
    DateChanged ,
    SoldTo  ,
    SoldPrice
) VALUES (
    5,
    'ENG PHYS 130 Textbook',
    'Tough course, so I took it out on the book a few times.',
    5,
    2,
    'Very Used',
    '2024-03-13 16:00:00'::TIMESTAMP,
    'S',
    '2024-03-15 16:00:00'::TIMESTAMP,
    8,
    1
);

/* Sale 4 - Mark (8) to Tim (7) */

INSERT INTO listing (
    UserID,
    ListingName ,
    ListingDescription ,
    AskingPrice ,
    CategoryTypeID,
    Condition ,
    DateListed,
    ListingStatus  ,
    DateChanged ,
    SoldTo  ,
    SoldPrice
) VALUES (
    8,
    'PHYS 130 Lab Kit',
    'Only used a few times...',
    20,
    3,
    'Very Good',
    '2024-03-14 20:00:00'::TIMESTAMP,
    'S',
    '2024-03-15 16:00:00'::TIMESTAMP,
    7,
    16
);

/* Sale 5 - Mark (8) to Alice (6) */

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
    8,
    'U of A Merch',
    'Size medium and never worn.',
    50,
    'New',
    '2024-03-15 12:00:00'::TIMESTAMP,
    'S',
    '2024-03-16 12:00:00'::TIMESTAMP,
    6,
    60
);