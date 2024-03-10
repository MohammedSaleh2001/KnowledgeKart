CREATE TABLE IF NOT EXISTS textbook (
    CategoryID SERIAL,
    Title varchar,
    Author varchar,
    PubYear int,
    Course varchar,
    PRIMARY KEY (CategoryID)
)