CREATE TABLE IF NOT EXISTS core.dim_condition (
    ConditionID SERIAL PRIMARY KEY,
    Condition varchar NOT NULL
);

INSERT INTO core.dim_condition (Condition) VALUES ('New');
INSERT INTO core.dim_condition (Condition) VALUES ('Very Good');
INSERT INTO core.dim_condition (Condition) VALUES ('Good');
INSERT INTO core.dim_condition (Condition) VALUES ('Used');
INSERT INTO core.dim_condition (Condition) VALUES ('Very Used');