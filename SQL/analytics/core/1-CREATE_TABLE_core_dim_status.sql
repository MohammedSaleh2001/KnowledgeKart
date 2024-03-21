CREATE TABLE IF NOT EXISTS core.dim_status (
    StatusID SERIAL PRIMARY KEY,
    Status char NOT NULL,
    StatusName varchar NOT NULL
);

INSERT INTO core.dim_status (Status, StatusName) VALUES ('O', 'Open');
INSERT INTO core.dim_status (Status, StatusName) VALUES ('C', 'Closed');
INSERT INTO core.dim_status (Status, StatusName) VALUES ('S', 'Sold');