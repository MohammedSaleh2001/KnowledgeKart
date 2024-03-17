import os
import psycopg2

DB_USER = "postgres"
DB_PASS = os.environ["POSTGRES_PASSWORD"]
DB_HOST = "postgres"
DB_PORT = "5432"

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
                        EXTRACT(year from u.DateJoined)*10000 
                        + EXTRACT('month' from u.DateJoined)*100
                        + EXTRACT('day' from u.DateJoined), 19000101) as DateJoinedFK,
                    COALESCE( to_char(u.DateJoined, 'hh24mi'), '-1' ) AS TimeJoinedFK,
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
                        EXTRACT(year from t.the_interval)*10000 
                        + EXTRACT('month' from t.the_interval)*100
                        + EXTRACT('day' from t.the_interval), 19000101) as DateFK,
                    COALESCE( to_char(t.the_interval, 'hh24mi'), '-1' ) AS TimeFK,
                    COUNT(n.UserID)
            FROM the_intervals t
            LEFT JOIN core.kkuser n ON (n.DateJoined >= t.the_interval AND n.DateJoined < t.the_interval + interval '3 hour')
            GROUP BY t.the_interval
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
                    EXTRACT(year from current_interval)*10000 
                    + EXTRACT('month' from current_interval)*100
                    + EXTRACT('day' from current_interval), 19000101) as DateFK,
                COALESCE( to_char(current_interval, 'hh24mi'), '-1' ) AS TimeFK,
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

def etl_user():
    try:
        m_conn = psycopg2.connect(database='main',
                                    user=DB_USER,
                                    password=DB_PASS,
                                    host=DB_HOST,
                                    port=DB_PORT)
        
        a_conn = psycopg2.connect(database='analytics',
                                        user=DB_USER,
                                        password=DB_PASS,
                                        host=DB_HOST,
                                        port=DB_PORT)
    except:
        print("Couldn't connect to DB for extract_user")

    deltas = get_user_delta(m_conn, a_conn)
    m_delta = deltas[0]
    a_delta = deltas[1]

    if m_delta is None or a_delta is None:
        print("Could not retrieve deltas...")
        m_conn.close()
        a_conn.close()
        return
    
    if m_delta == a_delta:
        print("No changes to Users!")
        m_conn.close()
        a_conn.close()
        return

    data = extract_transform_users(m_conn, a_delta)

    try:
        load_users(a_conn, data)
    except:
        print("Could not update Users!")
        m_conn.close()
        a_conn.close()
        return

    print("Successfully added Users!")

    # Do Datamart Work...
    try:
        datamart_newuserreport(a_conn)
        print("Completed New User Report!")
        datamart_userreport(a_conn)
        print("Completed User Report!")
    except:
        print("Could not complete User Reports!")
        m_conn.close()
        a_conn.close()
        return

    try:
        update_user_delta(a_conn)
    except:
        print("Could not update user delta!")
        m_conn.close()
        a_conn.close()
        return

    print("Updated user delta!")
    print("Work completed, closing connections...")
    m_conn.close()
    a_conn.close()
    return

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
                    l.DateListed,
                    COALESCE(
                        EXTRACT(year from l.DateListed)*10000 
                        + EXTRACT('month' from l.DateListed)*100
                        + EXTRACT('day' from l.DateListed), 19000101) as DateListedFK,
                    COALESCE( to_char(l.DateListed, 'hh24mi'), '-1' ) AS TimeListedFK,
                    l.ListingStatus,
                    l.DateChanged,
                    COALESCE(
                        EXTRACT(year from l.DateChanged)*10000 
                        + EXTRACT('month' from l.DateChanged)*100
                        + EXTRACT('day' from l.DateChanged), 19000101) as DateChangedFK,
                    COALESCE( to_char(l.DateChanged, 'hh24mi'), '-1' ) AS TimeChangedFK,
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
                  %s, %s, %s, %s, %s, %s)
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
            SELECT generate_series AS the_interval, CategoryTypeID, Category
            FROM generate_series(COALESCE (
                                    (SELECT MAX(NewListingReportDate) 
                                    FROM datamart.newlistingreport), '2024-03-10'::TIMESTAMP 
                                ), CURRENT_TIMESTAMP::timestamp, '3 hour'),
                core.dim_categorytype
        )
        INSERT INTO datamart.newlistingreport (
            NewListingReportDate ,
            NewListingReportDateFK ,
            NewListingReportTimeFK ,
            Category ,
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
                        EXTRACT(year from t.the_interval)*10000 
                        + EXTRACT('month' from t.the_interval)*100
                        + EXTRACT('day' from t.the_interval), 19000101) as DateFK,
                    COALESCE( to_char(t.the_interval, 'hh24mi'), '-1' ) AS TimeFK,
                    t.Category,
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
                                        AND l1.CategoryTypeID = t.CategoryTypeID)
            LEFT JOIN core.listing l2 ON (l2.DateChanged >= t.the_interval 
                                        AND l2.DateChanged < t.the_interval + interval '3 hour'
                                        AND l2.CategoryTypeID = t.CategoryTypeID
                                        AND l2.ListingStatus = 'C')
            LEFT JOIN core.listing l3 ON (l3.DateChanged >= t.the_interval 
                                        AND l3.DateChanged < t.the_interval + interval '3 hour'
                                        AND l3.CategoryTypeID = t.CategoryTypeID
                                        AND l3.ListingStatus = 'S')
            GROUP BY t.the_interval, t.Category
            ORDER BY t.the_interval, t.Category

        ) ON CONFLICT (NewListingReportDate, Category) DO UPDATE SET
            NewListingReportDate = EXCLUDED.NewListingReportDate,
            NewListingReportDateFK = EXCLUDED.NewListingReportDateFK,
            NewListingReportTimeFK = EXCLUDED.NewListingReportTimeFK,
            Category = EXCLUDED.Category,
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
                    EXTRACT(year from current_interval)*10000 
                    + EXTRACT('month' from current_interval)*100
                    + EXTRACT('day' from current_interval), 19000101) as DateFK,
                COALESCE( to_char(current_interval, 'hh24mi'), '-1' ) AS TimeFK,
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


def etl_listing():
    try:
        m_conn = psycopg2.connect(database='main',
                                    user=DB_USER,
                                    password=DB_PASS,
                                    host=DB_HOST,
                                    port=DB_PORT)
        
        a_conn = psycopg2.connect(database='analytics',
                                        user=DB_USER,
                                        password=DB_PASS,
                                        host=DB_HOST,
                                        port=DB_PORT)
    except:
        print("Couldn't connect to DB for extract_listing")

    # Get listing dependency category type
    try:
        get_dim_categorytype(m_conn, a_conn)
    except:
        print("Could not get category dimension!")
        m_conn.close()
        a_conn.close()
        return

    deltas = get_listing_delta(m_conn, a_conn)
    m_delta = deltas[0]
    a_delta = deltas[1]

    if m_delta is None or a_delta is None:
        print("Could not retrieve deltas...")
        m_conn.close()
        a_conn.close()
        return
    
    if m_delta == a_delta:
        print("No changes to Listing!")
        m_conn.close()
        a_conn.close()
        return

    data = extract_transform_listing(m_conn, a_delta)

    try:
        load_listing(a_conn, data)
    except Exception as e:
        print("Could not update Listing!")
        print(e)
        m_conn.close()
        a_conn.close()
        return

    print("Successfully added Listings!")

    # Do Datamart Work...
    try:
        datamart_newlistingreport(a_conn)
        print("Completed New Listing Report!")
        datamart_listingreport(a_conn)
        print("Completed Listing Report!")
    except:
        print("Could not complete Listing Reports!")
        m_conn.close()
        a_conn.close()
        return

    try:
        update_listing_delta(a_conn)
    except:
        print("Could not update Listing delta!")
        m_conn.close()
        a_conn.close()
        return

    print("Updated Listing delta!")
    print("Work completed, closing connections...")
    m_conn.close()
    a_conn.close()
    return


def main():
    etl_user()
    etl_listing()

if __name__ == "__main__":
    main()