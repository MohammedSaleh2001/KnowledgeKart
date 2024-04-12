import sys
import os
import unittest
import psycopg2

DB_USER = "postgres"
DB_PASS = "postgres"
DB_HOST = "127.0.0.1"
DB_PORT = "5432"

# Simulate the main and analytics database using the default "public" and "airflow" databases.

try:
    m_conn = psycopg2.connect(database='postgres',
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)

    a_conn = psycopg2.connect(database='airflow',
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)
    
    m_conn.autocommit = True
    a_conn.autocommit = True

    m_cursor = m_conn.cursor()
    a_cursor = a_conn.cursor()

except:
    print("Couldn't connect to DB")

# Get all ETL functions

def get_user_delta(m_conn, a_conn):
    m_cursor = m_conn.cursor()

    a_cursor = a_conn.cursor() 

    m_cursor.execute("SELECT MAX(UserID) FROM kkuser")

    main_max = m_cursor.fetchone()

    a_cursor.execute("SELECT MAX(UserID) FROM core.delta")

    analytics_max = a_cursor.fetchone()

    return main_max[0], analytics_max[0]
    
def extract_transform_users(m_conn, a_delta):
    m_cursor = m_conn.cursor()

    m_cursor.execute(
            '''
            SELECT  u.UserID,
                    u.Email,
                    u.FirstName,
                    u.DateJoined,
                    COALESCE(
                        EXTRACT(year from u.DateJoined AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*10000 
                        + EXTRACT('month' from u.DateJoined AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*100
                        + EXTRACT('day' from u.DateJoined AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton'), 19000101) as DateJoinedFK,
                    COALESCE( to_char(u.DateJoined AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton', 'hh24mi'), '-1' ) AS TimeJoinedFK,
                    u.UserRole,
                    u.Verified,
                    u.Blacklist,
                    u.Politeness,
                    u.Honesty,
                    u.Quickness,
                    u.NumReviews,
                    COALESCE(mt.cnt + mf.cnt, 0) as NumMessages,
                    COALESCE(nl.NumListings, 0) as NumListings,
                    COALESCE(nsl.NumSoldListings, 0) as NumSoldListings,
                    COALESCE(ncl.NumClosedListings, 0) as NumClosedListings,
                    COALESCE(nbl.NumListingsBought, 0) as NumListingsBought,
                    COALESCE(nr.NumReports, 0) as NumberOfReports,
                    (u.Honesty + u.Quickness + u.Politeness) / 3 as AvgUserRating
            FROM
            kkuser u
            LEFT JOIN (SELECT MessageTo as UserID, COUNT(*) as cnt
                    FROM chat
                    GROUP BY MessageTo) mt ON u.UserID = mt.UserID
            LEFT JOIN (SELECT MessageFrom as UserID, COUNT(*) as cnt
                    FROM chat
                    GROUP BY MessageFrom) mf ON u.UserID = mf.UserID
            LEFT JOIN (
                SELECT UserID, COUNT(*) AS NumListings
                FROM listing
                WHERE ListingStatus = 'O'
                GROUP BY UserID
            ) nl ON nl.UserID = u.UserID
            LEFT JOIN (
                SELECT UserID, COUNT(*) AS NumSoldListings
                FROM listing
                WHERE ListingStatus = 'S'
                GROUP BY UserID
            ) nsl ON nsl.UserID = u.UserID
            LEFT JOIN (
                SELECT UserID, COUNT(*) AS NumClosedListings
                FROM listing
                WHERE ListingStatus = 'C'
                GROUP BY UserID
            ) ncl ON ncl.UserID = u.UserID
            LEFT JOIN (
                SELECT SoldTo as UserID, COUNT(*) AS NumListingsBought
                FROM listing
                WHERE ListingStatus = 'S'
                GROUP BY SoldTo
            ) nbl ON nbl.UserID = u.UserID
            LEFT JOIN (
                SELECT ReportFor as UserID, COUNT(*) AS NumReports
                FROM report
                GROUP BY ReportFor
            ) nr ON nr.UserID = u.UserID
            WHERE u.UserID > %s
            '''
        , (a_delta,))
    
    return m_cursor.fetchall()

def load_users(a_conn, data):
    a_cursor = a_conn.cursor()

    # ON CONFLICT should never evaluate ideally
    a_cursor.executemany(
        '''
        INSERT INTO core.kkuser (
            UserID,
            Email, 
            FirstName,
            DateJoined ,
            DateJoinedFK ,
            TimeJoinedFK,
            UserRole,
            Verified ,
            Blacklist ,
            Politeness ,
            Honesty ,
            Quickness ,
            NumReviews ,
            NumberOfChats,
            NumberOfListings ,
            NumberOfSoldListings ,
            NumberOfClosedListings ,
            NumberOfBoughtListings ,
            NumberOfReports,
            AvgUserRating 
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (UserID) DO NOTHING;
        '''
        , data
    )

    a_conn.commit()

    return True

def datamart_newuserreport(a_conn):
    a_cursor = a_conn.cursor()

    a_cursor.execute(
        '''
        WITH the_intervals AS (
            SELECT generate_series AS the_interval
            FROM generate_series(COALESCE (
                                    (SELECT MAX(NewUserReportDate) 
                                    FROM datamart.newuserreport), '2024-03-10'::TIMESTAMP 
                                ), CURRENT_TIMESTAMP::timestamp, '3 hour')
        )
        INSERT INTO datamart.newuserreport (
            NewUserReportDate,
            NewUserReportDateFK ,
            NewUserReportTimeFK ,
            NumNewUsers 
        ) (

            SELECT t.the_interval,
                    COALESCE(
                        EXTRACT(year from t.the_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*10000 
                        + EXTRACT('month' from t.the_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*100
                        + EXTRACT('day' from t.the_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton'), 19000101) as DateFK,
                    COALESCE( to_char(t.the_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton', 'hh24mi'), '-1' ) AS TimeFK,
                    COUNT(n.UserID)
            FROM the_intervals t
            LEFT JOIN core.kkuser n ON (n.DateJoined >= t.the_interval AND n.DateJoined < t.the_interval + interval '3 hour')
            GROUP BY t.the_interval, DateFK, TimeFK
            ORDER BY t.the_interval
        ) ON CONFLICT (NewUserReportDate) DO UPDATE SET
            NewUserReportDate = EXCLUDED.NewUserReportDate,
            NewUserReportDateFK = EXCLUDED.NewUserReportDateFK,
            NewUserReportTimeFK = EXCLUDED.NewUserReportTimeFK,
            NumNewUsers = EXCLUDED.NumNewUsers
        '''
    )

    a_conn.commit()

    return True

def datamart_userreport(a_conn):
    a_cursor = a_conn.cursor()

    a_cursor.execute(
        '''
        WITH the_interval AS (
            SELECT 
            date_trunc('hour', CURRENT_TIMESTAMP::TIMESTAMP) 
            + date_part('minute', CURRENT_TIMESTAMP::TIMESTAMP)::int / 30 * interval '30 min'
            AS current_interval
        )
        INSERT INTO datamart.userreport (
            UserReportDate,
            UserReportDateFK ,
            UserReportTimeFK ,
            NumUnverifiedUsers ,
            NumVerifiedUsers ,
            NumBlacklistedUsers ,
            NumTotalUsers ,
            AvgUserRating 
        ) (
            SELECT current_interval,
                COALESCE(
                    EXTRACT(year from current_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*10000 
                    + EXTRACT('month' from current_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*100
                    + EXTRACT('day' from current_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton'), 19000101) as DateFK,
                COALESCE( to_char(current_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton', 'hh24mi'), '-1' ) AS TimeFK,
                COUNT(UserID) FILTER (WHERE Verified = False),
                COUNT(UserID) FILTER (WHERE Verified = True),
                COUNT(UserID) FILTER (WHERE Blacklist = True),
                COUNT(UserID),
                AVG(AvgUserRating) FILTER (WHERE AvgUserRating != 0)
            FROM the_interval, core.kkuser
            GROUP BY current_interval, DateFK, TimeFK

        ) ON CONFLICT (UserReportDate) DO UPDATE SET
            UserReportDate = EXCLUDED.UserReportDate,
            UserReportDateFK = EXCLUDED.UserReportDateFK,
            UserReportTimeFK = EXCLUDED.UserReportTimeFK,
            NumUnverifiedUsers = EXCLUDED.NumUnverifiedUsers,
            NumVerifiedUsers = EXCLUDED.NumVerifiedUsers,
            NumBlacklistedUsers = EXCLUDED.NumBlacklistedUsers,
            NumTotalUsers = EXCLUDED.NumTotalUsers,
            AvgUserRating = EXCLUDED.AvgUserRating
        '''
    )

    a_conn.commit()

    return True

def update_user_delta(a_conn):
    a_cursor = a_conn.cursor()

    # UserID should never be NULL if this function is called, only a contingency
    a_cursor.execute(
        '''
        UPDATE core.delta
        SET UserID = (
            SELECT COALESCE(MAX(UserID), 0)
            FROM core.kkuser
        )
        '''
    )

    a_conn.commit()

    return True

def get_dim_categorytype(m_conn, a_conn):
    m_cursor = m_conn.cursor()

    a_cursor = a_conn.cursor() 

    m_cursor.execute('SELECT * FROM categorytype')

    categories = m_cursor.fetchall()

    a_cursor.executemany('INSERT INTO core.dim_categorytype VALUES (%s, %s) ON CONFLICT (CategoryTypeID) DO NOTHING',
                         categories)
    
    a_conn.commit()

def get_listing_delta(m_conn, a_conn):
    m_cursor = m_conn.cursor()

    a_cursor = a_conn.cursor() 

    m_cursor.execute("SELECT MAX(ListingID) FROM listing")

    main_max = m_cursor.fetchone()

    a_cursor.execute("SELECT MAX(ListingID) FROM core.delta")

    analytics_max = a_cursor.fetchone()

    return main_max[0], analytics_max[0]
    
def extract_transform_listing(m_conn, a_delta):
    m_cursor = m_conn.cursor()

    m_cursor.execute(
            '''
            SELECT  l.ListingID,
                    l.UserID,
                    l.AskingPrice,
                    l.CategoryTypeID,
                    l.CategoryID,
                    l.Condition,
                    l.DateListed,
                    COALESCE(
                        EXTRACT(year from l.DateListed AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*10000 
                        + EXTRACT('month' from l.DateListed AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*100
                        + EXTRACT('day' from l.DateListed AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton'), 19000101) as DateListedFK,
                    COALESCE( to_char(l.DateListed AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton', 'hh24mi'), '-1' ) AS TimeListedFK,
                    l.ListingStatus,
                    l.DateChanged,
                    COALESCE(
                        EXTRACT(year from l.DateChanged AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*10000 
                        + EXTRACT('month' from l.DateChanged AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*100
                        + EXTRACT('day' from l.DateChanged AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton'), 19000101) as DateChangedFK,
                    COALESCE( to_char(l.DateChanged AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton', 'hh24mi'), '-1' ) AS TimeChangedFK,
                    l.SoldTo,
                    l.SoldPrice,
                    CASE WHEN l.ListingStatus = 'O' THEN -1
                         ELSE EXTRACT('day' FROM (l.DateChanged - l.DateListed)) * 24 * 60 
                            + EXTRACT('hour' FROM (l.DateChanged- l.DateListed)) * 60
                            + EXTRACT('minute' FROM (l.DateChanged - l.DateListed)) 
                    END as TimeToClose,
                    CASE WHEN l.ListingStatus != 'S' THEN -999999
                         ELSE l.AskingPrice - l.SoldPrice
                    END as DifferenceAskingSoldPrice
            FROM listing l
            WHERE l.ListingID > %s
            '''
        , (a_delta,))
    
    return m_cursor.fetchall()

def load_listing(a_conn, data):
    a_cursor = a_conn.cursor()

    # ON CONFLICT should never evaluate ideally
    a_cursor.executemany(
        '''
        INSERT INTO core.listing (
            ListingID ,
            UserID ,
            AskingPrice ,
            CategoryTypeID ,
            CategoryID ,
            Condition,
            DateListed,
            DateListedFK ,
            TimeListedFK ,
            ListingStatus,
            DateChanged ,
            DateChangedFK ,
            TimeChangedFK ,
            SoldTo ,
            SoldPrice ,
            TimeToClose ,
            DifferenceAskingSoldPrice 
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (ListingID) DO NOTHING;
        '''
        , data
    )

    a_conn.commit()

    return True

def datamart_newlistingreport(a_conn):
    a_cursor = a_conn.cursor()

    a_cursor.execute(
        '''
        WITH the_intervals AS (
            SELECT generate_series AS the_interval, CategoryTypeID, Category, Condition
            FROM generate_series(COALESCE (
                                    (SELECT MAX(NewListingReportDate) 
                                    FROM datamart.newlistingreport), '2024-03-10'::TIMESTAMP 
                                ), CURRENT_TIMESTAMP::timestamp, '3 hour'),
                core.dim_categorytype, core.dim_condition
        )
        INSERT INTO datamart.newlistingreport (
            NewListingReportDate ,
            NewListingReportDateFK ,
            NewListingReportTimeFK ,
            Category ,
            Condition,
            NumNewListings ,
            NumClosedListings ,
            NumSoldListings ,
            AverageCloseTime ,
            AverageSellTime ,
            AveragePriceSaleDifference ,
            AveragePercentSaleDifference 
        ) (

            SELECT t.the_interval,
                    COALESCE(
                        EXTRACT(year from t.the_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*10000 
                        + EXTRACT('month' from t.the_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*100
                        + EXTRACT('day' from t.the_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton'), 19000101) as DateFK,
                    COALESCE( to_char(t.the_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton', 'hh24mi'), '-1' ) AS TimeFK,
                    t.Category,
					t.Condition,
                    COUNT(l1.ListingID) as NumNewListings,
                    COUNT(l2.ListingID) as NumClosedListings,
                    COUNT(l3.ListingID) as NumSoldListings,
                    COALESCE(AVG(l2.TimeToClose), -1) as AverageCloseTime,
                    COALESCE(AVG(l3.TimeToClose), -1) as AverageSellTime,
                    COALESCE(AVG(l3.DifferenceAskingSoldPrice), -999999) as AveragePriceSaleDifference,
                    COALESCE(AVG(l3.SoldPrice / l3.AskingPrice) * 100, -1) as AveragePercentSaleDifference
            FROM the_intervals t
            LEFT JOIN core.listing l1 ON (l1.DateListed >= t.the_interval 
                                        AND l1.DateListed < t.the_interval + interval '3 hour'
                                        AND l1.CategoryTypeID = t.CategoryTypeID
										AND l1.Condition = t.Condition)
            LEFT JOIN core.listing l2 ON (l2.DateChanged >= t.the_interval 
                                        AND l2.DateChanged < t.the_interval + interval '3 hour'
                                        AND l2.CategoryTypeID = t.CategoryTypeID
                                        AND l2.ListingStatus = 'C'
										AND l2.Condition = t.Condition)
            LEFT JOIN core.listing l3 ON (l3.DateChanged >= t.the_interval 
                                        AND l3.DateChanged < t.the_interval + interval '3 hour'
                                        AND l3.CategoryTypeID = t.CategoryTypeID
                                        AND l3.ListingStatus = 'S'
									    AND l3.Condition = t.Condition)
            GROUP BY t.the_interval, DateFK, TimeFK, t.Category, t.Condition
            ORDER BY t.the_interval, t.Category

        ) ON CONFLICT (NewListingReportDate, Category, Condition) DO UPDATE SET
            NewListingReportDate = EXCLUDED.NewListingReportDate,
            NewListingReportDateFK = EXCLUDED.NewListingReportDateFK,
            NewListingReportTimeFK = EXCLUDED.NewListingReportTimeFK,
            Category = EXCLUDED.Category,
            Condition = EXCLUDED.Condition,
            NumNewListings = EXCLUDED.NumNewListings,
            NumClosedListings = EXCLUDED.NumClosedListings,
            NumSoldListings= EXCLUDED.NumSoldListings ,
            AverageCloseTime = EXCLUDED.AverageCloseTime,
            AverageSellTime = EXCLUDED.AverageSellTime,
            AveragePriceSaleDifference = EXCLUDED.AveragePriceSaleDifference,
            AveragePercentSaleDifference = EXCLUDED.AveragePercentSaleDifference
            ;
        '''
    )

    a_conn.commit()

    return True

def datamart_listingreport(a_conn):
    a_cursor = a_conn.cursor()

    a_cursor.execute(
        '''
        WITH the_interval AS (
            SELECT 
            date_trunc('hour', CURRENT_TIMESTAMP::TIMESTAMP) 
            + date_part('minute', CURRENT_TIMESTAMP::TIMESTAMP)::int / 30 * interval '30 min'
            AS current_interval
        )
        INSERT INTO datamart.listingreport (
            ListingReportDate,
            ListingReportDateFK ,
            ListingReportTimeFK ,
            NumOpenListings ,
            NumClosedListings ,
            NumSoldListings 
        ) (
            SELECT current_interval,
                COALESCE(
                    EXTRACT(year from current_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*10000 
                    + EXTRACT('month' from current_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*100
                    + EXTRACT('day' from current_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton'), 19000101) as DateFK,
                COALESCE( to_char(current_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton', 'hh24mi'), '-1' ) AS TimeFK,
                COUNT(ListingID) FILTER (WHERE ListingStatus = 'O'),
                COUNT(ListingID) FILTER (WHERE ListingStatus = 'C'),
                COUNT(ListingID) FILTER (WHERE ListingStatus = 'S')
            FROM the_interval, core.listing
            GROUP BY current_interval, DateFK, TimeFK

        ) ON CONFLICT (ListingReportDate) DO UPDATE SET
            ListingReportDate = EXCLUDED.ListingReportDate,
            ListingReportDateFK  = EXCLUDED.ListingReportDateFK,
            ListingReportTimeFK  = EXCLUDED.ListingReportTimeFK,
            NumOpenListings  = EXCLUDED.NumOpenListings,
            NumClosedListings  = EXCLUDED.NumClosedListings,
            NumSoldListings  = EXCLUDED.NumSoldListings

        '''
    )

    a_conn.commit()

    return True

def update_listing_delta(a_conn):
    a_cursor = a_conn.cursor()

    # UserID should never be NULL if this function is called, only a contingency
    a_cursor.execute(
        '''
        UPDATE core.delta
        SET ListingID = (
            SELECT COALESCE(MAX(ListingID), 0)
            FROM core.listing
        )
        '''
    )

    a_conn.commit()

    return True


def get_report_delta(m_conn, a_conn):
    m_cursor = m_conn.cursor()

    a_cursor = a_conn.cursor() 

    m_cursor.execute("SELECT MAX(ReportID) FROM report")

    main_max = m_cursor.fetchone()

    a_cursor.execute("SELECT MAX(ReportID) FROM core.delta")

    analytics_max = a_cursor.fetchone()

    return main_max[0], analytics_max[0]
    
def extract_transform_report(m_conn, a_delta):
    m_cursor = m_conn.cursor()

    m_cursor.execute(
            '''
            SELECT  r.ReportID,
                    r.ReportBy,
                    r.ReportFor,
                    r.DateReported,
                    COALESCE(
                        EXTRACT(year from r.DateReported AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*10000 
                        + EXTRACT('month' from r.DateReported AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*100
                        + EXTRACT('day' from r.DateReported AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton'), 19000101) as DateReportedFK,
                    COALESCE( to_char(r.DateReported AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton', 'hh24mi'), '-1' ) AS TimeReportedFK,
                    r.ModeratorAssigned,
                    r.ReportOpen,
                    r.DateClosed,
                    COALESCE(
                        EXTRACT(year from r.DateClosed AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*10000 
                        + EXTRACT('month' from r.DateClosed AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*100
                        + EXTRACT('day' from r.DateClosed AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton'), 19000101) as DateClosedFK,
                    COALESCE( to_char(r.DateClosed AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton', 'hh24mi'), '-1' ) AS TimeClosedFK,
                    CASE WHEN r.ReportOpen = True THEN -1
                        ELSE EXTRACT('day' FROM (r.DateClosed - r.DateReported)) * 24 * 60 
                            + EXTRACT('hour' FROM (r.DateClosed- r.DateReported)) * 60
                            + EXTRACT('minute' FROM (r.DateClosed - r.DateReported)) 
                    END as TimeToClose
            FROM report r
            WHERE r.ReportID > %s
            '''
        , (a_delta,))
    
    return m_cursor.fetchall()

def load_report(a_conn, data):
    a_cursor = a_conn.cursor()

    # ON CONFLICT should never evaluate ideally
    a_cursor.executemany(
        '''
        INSERT INTO core.report (
            ReportID,
            ReportBy ,
            ReportFor,
            DateReported ,
            DateReportedFK ,
            TimeReportedFK ,
            ModeratorAssigned,
            ReportOpen ,
            DateClosed ,
            DateClosedFK ,
            TimeClosedFK ,
            TimeToClose 
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s)
        ON CONFLICT (ReportID) DO NOTHING;
        '''
        , data
    )

    a_conn.commit()

    return True

def datamart_newmodreport(a_conn):
    a_cursor = a_conn.cursor()

    a_cursor.execute(
        '''
        WITH the_intervals AS (
            SELECT generate_series AS the_interval
            FROM generate_series(COALESCE (
                                    (SELECT MAX(NewModReportDate) 
                                    FROM datamart.newmodreport), '2024-03-10'::TIMESTAMP 
                                ), CURRENT_TIMESTAMP::timestamp, '3 hour')
        )
        INSERT INTO datamart.newmodreport (
            NewModReportDate,
            NewModReportDateFK ,
            NewModReportTimeFK ,
            NumNewReports ,
            NumClosedReports ,
            AverageTimeToClose 
        ) (

            SELECT t.the_interval,
                    COALESCE(
                        EXTRACT(year from t.the_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*10000 
                        + EXTRACT('month' from t.the_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*100
                        + EXTRACT('day' from t.the_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton'), 19000101) as DateFK,
                    COALESCE( to_char(t.the_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton', 'hh24mi'), '-1' ) AS TimeFK,
                    COUNT(r1.ReportID) as NumNewReports,
                    COUNT(r2.ReportID) as NumClosedReports,
                    COALESCE(AVG(r1.TimeToClose), -1) as AverageCloseTime
            FROM the_intervals t
            LEFT JOIN core.report r1 ON (r1.DateReported >= t.the_interval 
                                        AND r1.DateReported < t.the_interval + interval '3 hour')
            LEFT JOIN core.report r2 ON (r2.DateClosed >= t.the_interval 
                                        AND r2.DateClosed < t.the_interval + interval '3 hour')
            GROUP BY t.the_interval, DateFK, TimeFK
            ORDER BY t.the_interval

        ) ON CONFLICT (NewModReportDate) DO UPDATE SET
            NewModReportDate= EXCLUDED.NewModReportDate,
            NewModReportDateFK = EXCLUDED.NewModReportDateFK,
            NewModReportTimeFK = EXCLUDED.NewModReportTimeFK,
            NumNewReports = EXCLUDED.NumNewReports,
            NumClosedReports = EXCLUDED.NumClosedReports,
            AverageTimeToClose = EXCLUDED.AverageTimeToClose
            ;
        '''
    )

    a_conn.commit()

    return True

def datamart_modreport(a_conn):
    a_cursor = a_conn.cursor()

    a_cursor.execute(
        '''
        WITH the_interval AS (
            SELECT 
            date_trunc('hour', CURRENT_TIMESTAMP::TIMESTAMP) 
            + date_part('minute', CURRENT_TIMESTAMP::TIMESTAMP)::int / 30 * interval '30 min'
            AS current_interval
        )
        INSERT INTO datamart.modreport (
            ModReportDate ,
            ModReportDateFK ,
            ModReportTimeFK ,
            NumOpenReports ,
            NumUnassignedReports ,
            NumClosedReports ,
            NumTotalReports 
        ) (
            SELECT current_interval,
                COALESCE(
                    EXTRACT(year from current_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*10000 
                    + EXTRACT('month' from current_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton')*100
                    + EXTRACT('day' from current_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton'), 19000101) as DateFK,
                COALESCE( to_char(current_interval AT TIME ZONE 'UTC' AT TIME ZONE 'America/Edmonton', 'hh24mi'), '-1' ) AS TimeFK,
                COUNT(ReportID) FILTER (WHERE ReportOpen = True) AS NumOpenReports,
                COUNT(ReportID) FILTER (WHERE ModeratorAssigned IS NULL) AS NumUnassignedReports,
                COUNT(ReportID) FILTER (WHERE ReportOpen = False) AS NumClosedReports,
                COUNT(ReportID) AS NumTotalReports
            FROM the_interval, core.report
            GROUP BY current_interval, DateFK, TimeFK

        ) ON CONFLICT (ModReportDate) DO UPDATE SET
            ModReportDate= EXCLUDED.ModReportDate,
            ModReportDateFK = EXCLUDED.ModReportDateFK,
            ModReportTimeFK = EXCLUDED.ModReportTimeFK,
            NumOpenReports = EXCLUDED.NumOpenReports,
            NumUnassignedReports = EXCLUDED.NumUnassignedReports,
            NumClosedReports = EXCLUDED.NumClosedReports,
            NumTotalReports = EXCLUDED.NumTotalReports
            ;
        '''
    )

    a_conn.commit()

    return True

def update_report_delta(a_conn):
    a_cursor = a_conn.cursor()

    # UserID should never be NULL if this function is called, only a contingency
    a_cursor.execute(
        '''
        UPDATE core.delta
        SET ReportID = (
            SELECT COALESCE(MAX(ReportID), 0)
            FROM core.report
        )
        '''
    )

    a_conn.commit()

    return True


class TestETL(unittest.TestCase):

    def test_a_get_delta(self):
        main_max, a_delta = get_user_delta(m_conn, a_conn)
        self.assertEqual(main_max, 8)
        self.assertEqual(a_delta, 0)

    def test_b_extract_transform_users(self):
        data = extract_transform_users(m_conn, 0)
        joe = data[3]

        self.assertEqual(joe[9], 2.0)
        self.assertEqual(joe[10], 4.0)
        self.assertEqual(joe[11], 5.0)
        self.assertEqual(joe[12], 1)

    def test_c_load_users(self):

        data = extract_transform_users(m_conn, 0)

        load_users(a_conn, data)

        a_cursor.execute("SELECT Politeness, Honesty, Quickness, NumReviews FROM core.kkuser WHERE email = 'joe@ualberta.ca'")

        result = a_cursor.fetchone()

        self.assertEqual(result[0], 2.0)
        self.assertEqual(result[1], 4.0)
        self.assertEqual(result[2], 5.0)
        self.assertEqual(result[3], 1)

    def test_d_newuserreport(self):
        data = extract_transform_users(m_conn, 0)

        load_users(a_conn, data)

        datamart_newuserreport(a_conn)

        # Three users joined at midnight UTC
        a_cursor.execute("SELECT NumNewUsers FROM datamart.newuserreport WHERE NewUserReportDate = '2024-03-11 00:00:00'::TIMESTAMP")

        result = a_cursor.fetchone()

        self.assertEqual(result[0], 3)

    def test_e_userreport(self):
        data = extract_transform_users(m_conn, 0)

        load_users(a_conn, data)

        datamart_userreport(a_conn)

        a_cursor.execute('''
                         SELECT NumUnverifiedUsers, NumVerifiedUsers, NumBlacklistedUsers, NumTotalUsers, AvgUserRating
                         FROM datamart.userreport 
                         ORDER BY UserReportDate DESC
                         LIMIT 1
                         ''')

        result = a_cursor.fetchone()

        # 8 users verified, 8 total, avg rating 3.4
        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], 8)
        self.assertEqual(result[2], 0)
        self.assertEqual(result[3], 8)
        self.assertAlmostEqual(float(result[4]), 3.4)

    def test_f_update_delta(self):

        update_user_delta(a_conn)

        a_cursor.execute('''
                         SELECT UserID FROM core.delta
                         ''')

        result = a_cursor.fetchone()

        self.assertEqual(result[0], 8)

    def test_g_get_dimcategorytype(self):

        get_dim_categorytype(m_conn, a_conn)

        a_cursor.execute('''
                         SELECT Category FROM core.dim_categorytype
                         ''')

        result = a_cursor.fetchall()
        
        self.assertEqual(result[0][0], 'Other')
        self.assertEqual(result[1][0], 'Textbook')
        self.assertEqual(result[2][0], 'Lab Equipment')


    def test_h_get_delta(self):
        main_max, a_delta = get_listing_delta(m_conn, a_conn)
        self.assertEqual(main_max, 6)
        self.assertEqual(a_delta, 0)

    def test_i_extract_transform_listing(self):
        data = extract_transform_listing(m_conn, 0)

        # Sale from Bob to Tim, History 100 textbook. Asked for 10, sold for 5, 2 and 2/3 days later.
        listing3 = data[2]
        
        self.assertEqual(listing3[15], 3840)
        self.assertEqual(listing3[16], 5)

    def test_j_load_listing(self):


        data = extract_transform_listing(m_conn, 0)

        load_listing(a_conn, data)

        a_cursor.execute("SELECT TimeToClose, DifferenceAskingSoldPrice FROM core.listing WHERE ListingID = 3")

        result = a_cursor.fetchone()

        self.assertEqual(result[0], 3840)
        self.assertEqual(result[1], 5)

    def test_k_newlistingreport(self):


        datamart_newlistingreport(a_conn)

        # One new textbook listing sold at 12 UTC on the 13th of March
        a_cursor.execute('''SELECT NumSoldListings, AverageSellTime, AveragePriceSaleDifference, AveragePercentSaleDifference 
                         FROM datamart.newlistingreport 
                         WHERE NewListingReportDate = '2024-03-13 12:00:00'::TIMESTAMP
                         AND Category = 'Textbook'
                         AND Condition = 'New' ''')

        result = a_cursor.fetchone()

        self.assertEqual(result[0], 1)
        self.assertEqual(float(result[1]), 2160.0)
        self.assertEqual(float(result[2]), 0.0)
        self.assertEqual(float(result[3]), 100.0)

    def test_l_listingreport(self):


        datamart_listingreport(a_conn)

        # One new textbook listing sold at 12 UTC on the 13th of March
        a_cursor.execute('''SELECT NumOpenListings, NumClosedListings, NumSoldListings
                         FROM datamart.listingreport 
                         ORDER BY ListingReportDate DESC
                         LIMIT 1 ''')

        result = a_cursor.fetchone()

        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 0)
        self.assertEqual(result[2], 5)

    def test_m_update_delta(self):

        update_listing_delta(a_conn)

        a_cursor.execute('''
                         SELECT ListingID FROM core.delta
                         ''')

        result = a_cursor.fetchone()

        self.assertEqual(result[0], 6)

    def test_n_get_delta(self):
        main_max, a_delta = get_report_delta(m_conn, a_conn)
        self.assertEqual(main_max, 1)
        self.assertEqual(a_delta, 0)

    def test_o_extract_transform_report(self):
        data = extract_transform_report(m_conn, 0)

        report = data[0]
        
        # Time to close report
        self.assertEqual(report[11], 210)

    def test_p_load_report(self):


        data = extract_transform_report(m_conn, 0)

        load_report(a_conn, data)

        a_cursor.execute("SELECT TimeToClose FROM core.report WHERE ReportID = 1")

        result = a_cursor.fetchone()

        self.assertEqual(result[0], 210)

    def test_q_newmoderationreport(self):


        datamart_newmodreport(a_conn)

        # 1 report was opened in between 12 and 15 UTC and took an average of 210 minutes to close
        a_cursor.execute('''SELECT NumNewReports, AverageTimeToCLose
                         FROM datamart.newmodreport 
                         WHERE NewModReportDate = '2024-03-13 12:00:00'::TIMESTAMP ''')

        result = a_cursor.fetchone()

        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 210)

    def test_r_modreport(self):


        datamart_modreport(a_conn)

        # One new textbook listing sold at 12 UTC on the 13th of March
        a_cursor.execute('''SELECT NumOpenReports, NumUnassignedReports, NumClosedReports, NumTotalReports
                         FROM datamart.modreport 
                         ORDER BY ModReportDate DESC
                         LIMIT 1 ''')

        result = a_cursor.fetchone()

        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], 0)
        self.assertEqual(result[2], 1)
        self.assertEqual(result[3], 1)

    def test_s_update_delta(self):

        update_report_delta(a_conn)

        a_cursor.execute('''
                         SELECT ReportID FROM core.delta
                         ''')

        result = a_cursor.fetchone()

        self.assertEqual(result[0], 1)


if __name__ == '__main__':

    # Setup the databases for testing
    etl_folder = os.getcwd()
    test_suite_folder = os.path.abspath(os.path.join(etl_folder, os.pardir))
    knowledge_kart = os.path.abspath(os.path.join(test_suite_folder, os.pardir))
    main = knowledge_kart + "/SQL/main"
    core = knowledge_kart + "/SQL/analytics/core"
    datamart = knowledge_kart + "/SQL/analytics/datamart"
    sample = knowledge_kart + "/SQL/sample"

    m_cursor.execute('DROP SCHEMA public CASCADE; CREATE SCHEMA IF NOT EXISTS public;')

    a_cursor.execute(
        'DROP SCHEMA core CASCADE; DROP SCHEMA datamart CASCADE; CREATE SCHEMA IF NOT EXISTS core; CREATE SCHEMA IF NOT EXISTS datamart;'
    )

    for filename in os.listdir(main):
        f = os.path.join(main, filename)

        m_cursor.execute(open(f, "r").read())

    for filename in os.listdir(core):
        f = os.path.join(core, filename)

        a_cursor.execute(open(f, "r").read())

    for filename in os.listdir(datamart):
        f = os.path.join(datamart, filename)

        a_cursor.execute(open(f, "r").read())

    for filename in os.listdir(sample):
        f = os.path.join(sample, filename)

        m_cursor.execute(open(f, "r").read())


    unittest.main(exit=False)

    m_cursor.execute('DROP SCHEMA public CASCADE; CREATE SCHEMA IF NOT EXISTS public;')

    a_cursor.execute(
        'DROP SCHEMA core CASCADE; DROP SCHEMA datamart CASCADE;'
    )