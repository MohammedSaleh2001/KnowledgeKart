/* Derived from Nikolai Schuler's date dimension table */

DO
$do$
BEGIN

    IF (NOT EXISTS (SELECT * 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_SCHEMA = 'core' 
                    AND  TABLE_NAME = 'dim_date') ) 
                    
    THEN

        CREATE TABLE core.dim_date
        (
        date_key              INT NOT NULL,
        date              	DATE NOT NULL,
        weekday               VARCHAR(9) NOT NULL,
        weekday_num           INT NOT NULL,
        day_month             INT NOT NULL,
        day_of_year           INT NOT NULL,
        week_of_year          INT NOT NULL,
        iso_week         		CHAR(10) NOT NULL,
        month_num             INT NOT NULL,
        month_name            VARCHAR(9) NOT NULL,
        month_name_short   	CHAR(3) NOT NULL,
        quarter      			INT NOT NULL,
        year              	INT NOT NULL,
        first_day_of_month    DATE NOT NULL,
        last_day_of_month     DATE NOT NULL,
        yyyymm                CHAR(7) NOT NULL,
        weekend_indr          CHAR(10) NOT NULL
        );

        ALTER TABLE core.dim_date ADD CONSTRAINT dim_date_pk PRIMARY KEY (date_key);

        CREATE INDEX d_date_date_actual_idx
        ON core.dim_date(date);

        INSERT INTO core.dim_date VALUES (
            19000101,
            '1900-01-01',
            'Monday',
            1,
            1,
            1,
            1,
            '1900-W01-1',
            1,
            'January',
            'Jan',
            1,
            1900,
            '1900-01-01',
            '1900-01-31',
            '1900-01',
            'weekday'
        );

        INSERT INTO core.dim_date
        SELECT TO_CHAR(datum, 'yyyymmdd')::INT AS date_key,
            datum AS date,
            TO_CHAR(datum, 'TMDay') AS weekday,
            EXTRACT(ISODOW FROM datum) AS weekday_num,
            EXTRACT(DAY FROM datum) AS day_month,
            EXTRACT(DOY FROM datum) AS day_of_year,
            EXTRACT(WEEK FROM datum) AS week_of_year,
            EXTRACT(ISOYEAR FROM datum) || TO_CHAR(datum, '"-W"IW-') || EXTRACT(ISODOW FROM datum) AS iso_week,
            EXTRACT(MONTH FROM datum) AS month,
            TO_CHAR(datum, 'TMMonth') AS month_name,
            TO_CHAR(datum, 'Mon') AS month_name_short,
            EXTRACT(QUARTER FROM datum) AS quarter,
            EXTRACT(YEAR FROM datum) AS year,
            datum + (1 - EXTRACT(DAY FROM datum))::INT AS first_day_of_month,
            (DATE_TRUNC('MONTH', datum) + INTERVAL '1 MONTH - 1 day')::DATE AS last_day_of_month,
            CONCAT(TO_CHAR(datum, 'yyyy'),'-',TO_CHAR(datum, 'mm')) AS mmyyyy,
            CASE
                WHEN EXTRACT(ISODOW FROM datum) IN (6, 7) THEN 'weekend'
                ELSE 'weekday'
                END AS weekend_indr
        FROM (SELECT '2010-01-01'::DATE + SEQUENCE.DAY AS datum
            FROM GENERATE_SERIES(0, 7300) AS SEQUENCE (DAY)
            GROUP BY SEQUENCE.DAY) DQ
        ORDER BY 1;

    END IF;
END
$do$