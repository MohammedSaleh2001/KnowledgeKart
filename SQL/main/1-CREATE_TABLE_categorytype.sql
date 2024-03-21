CREATE TABLE IF NOT EXISTS categorytype (
    CategoryTypeID SERIAL PRIMARY KEY,
    Category varchar NOT NULL
);

INSERT INTO categorytype (Category) VALUES ('Other');
INSERT INTO categorytype (Category) VALUES ('Textbook');
INSERT INTO categorytype (Category) VALUES ('Lab Equipment');
