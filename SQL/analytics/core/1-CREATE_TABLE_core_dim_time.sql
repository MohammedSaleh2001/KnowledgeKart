/* Derived from: https://wiki.postgresql.org/wiki/Date_and_Time_dimensions */

DO
$do$
BEGIN

    IF (NOT EXISTS (SELECT * 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_SCHEMA = 'core' 
                    AND  TABLE_NAME = 'dim_time') ) 
                    
    THEN

        CREATE TABLE core.dim_time
        (
        time_key              text NOT NULL,
        time                  text NOT NULL,
        hour              	  double precision NOT NULL,
        quarterhour           text NOT NULL,
        minute                double precision NULL,
        daytime               text NOT NULL,
        daynight              text NOT NULL
        );

        ALTER TABLE core.dim_time ADD CONSTRAINT dim_time_pk PRIMARY KEY (time_key);

        INSERT INTO core.dim_time VALUES (
            '-1',
            '-1',
            0,
            '0',
            '0',
            'None',
            'None'
        );

        INSERT INTO core.dim_time
        select to_char(minute, 'hh24mi') as time_key,
            to_char(minute, 'hh24:mi') AS time,
            -- Hour of the day (0 - 23)
            extract(hour from minute) as hour, 
            -- Extract and format quarter hours
            to_char(minute - (extract(minute from minute)::integer % 15 || 'minutes')::interval, 'hh24:mi') ||
            ' - ' ||
            to_char(minute - (extract(minute from minute)::integer % 15 || 'minutes')::interval + '14 minutes'::interval, 'hh24:mi')
                as quarterhour,
            -- Minute of the day (0 - 1439)
            extract(hour from minute)*60 + extract(minute from minute) as minute,
            -- Names of day periods
            case when to_char(minute, 'hh24:mi') between '06:00' and '08:29'
                then 'Morning'
                when to_char(minute, 'hh24:mi') between '08:30' and '11:59'
                then 'AM'
                when to_char(minute, 'hh24:mi') between '12:00' and '17:59'
                then 'PM'
                when to_char(minute, 'hh24:mi') between '18:00' and '22:29'
                then 'Evening'
                else 'Night'
            end as daytime,
            -- Indicator of day or night
            case when to_char(minute, 'hh24:mi') between '07:00' and '19:59' then 'Day'
                else 'Night'
            end AS daynight
        from (SELECT '0:00'::time + (sequence.minute || ' minutes')::interval AS minute
            FROM generate_series(0,1439) AS sequence(minute)
            GROUP BY sequence.minute
            ) DQ
        order by 1;

    END IF;
END
$do$