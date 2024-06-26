import os
import psycopg2

DB_USER = "postgres"
DB_PASS = os.environ["POSTGRES_PASSWORD"]
DB_HOST = "postgres"
DB_PORT = "5432"

# FR22
def get_user_delta(m_conn, a_conn):
    m_cursor = m_conn.cursor()

    a_cursor = a_conn.cursor() 

    m_cursor.execute("SELECT MAX(UserID) FROM kkuser")

    main_max = m_cursor.fetchone()

    a_cursor.execute("SELECT MAX(UserID) FROM core.delta")

    analytics_max = a_cursor.fetchone()

    return main_max[0], analytics_max[0]

# FR22
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

# FR22
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

# FR23
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

# FR23
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

# FR22
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

# FR22 / FR23
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
        try:
            datamart_newuserreport(a_conn)
            datamart_userreport(a_conn)
        except:
            print("Could not complete User Reports!")
            m_conn.close()
            a_conn.close()
            return
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

    

    # Do Datamart Work...
    try:
        datamart_newuserreport(a_conn)
        datamart_userreport(a_conn)
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

    print("Successfully added Users!")
    m_conn.close()
    a_conn.close()
    return


# FR21
def get_dim_categorytype(m_conn, a_conn):
    m_cursor = m_conn.cursor()

    a_cursor = a_conn.cursor() 

    m_cursor.execute('SELECT * FROM categorytype')

    categories = m_cursor.fetchall()

    a_cursor.executemany('INSERT INTO core.dim_categorytype VALUES (%s, %s) ON CONFLICT (CategoryTypeID) DO NOTHING',
                         categories)
    
    a_conn.commit()

# FR22
def get_listing_delta(m_conn, a_conn):
    m_cursor = m_conn.cursor()

    a_cursor = a_conn.cursor() 

    m_cursor.execute("SELECT MAX(ListingID) FROM listing")

    main_max = m_cursor.fetchone()

    a_cursor.execute("SELECT MAX(ListingID) FROM core.delta")

    analytics_max = a_cursor.fetchone()

    return main_max[0], analytics_max[0]

# FR22    
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

# FR22
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

# FR23
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

# FR23
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

# FR22
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

# FR22 / FR23
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
        try:
            datamart_newlistingreport(a_conn)
            datamart_listingreport(a_conn)
        except:
            print("Could not complete Listing Reports!")
            m_conn.close()
            a_conn.close()
            return
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

    

    # Do Datamart Work...
    try:
        datamart_newlistingreport(a_conn)
        datamart_listingreport(a_conn)
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

    print("Successfully added Listings!")
    m_conn.close()
    a_conn.close()
    return

# FR22
def get_report_delta(m_conn, a_conn):
    m_cursor = m_conn.cursor()

    a_cursor = a_conn.cursor() 

    m_cursor.execute("SELECT MAX(ReportID) FROM report")

    main_max = m_cursor.fetchone()

    a_cursor.execute("SELECT MAX(ReportID) FROM core.delta")

    analytics_max = a_cursor.fetchone()

    return main_max[0], analytics_max[0]

# FR22    
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

# FR22
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

# FR23
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

# FR23
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

# FR22
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

# FR22 / FR23
def etl_report():
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

    deltas = get_report_delta(m_conn, a_conn)
    m_delta = deltas[0]
    a_delta = deltas[1]

    if m_delta is None or a_delta is None:
        print("Could not retrieve deltas...")
        m_conn.close()
        a_conn.close()
        return
    
    if m_delta == a_delta:
        print("No changes to Reports!")
        try:
            datamart_newmodreport(a_conn)
            datamart_modreport(a_conn)
        except:
            print("Could not complete Mod Reports!")
            m_conn.close()
            a_conn.close()
            return
        m_conn.close()
        a_conn.close()
        return

    data = extract_transform_report(m_conn, a_delta)

    try:
        load_report(a_conn, data)
    except:
        print("Could not update Report!")
        m_conn.close()
        a_conn.close()
        return

    # Do Datamart Work...
    try:
        datamart_newmodreport(a_conn)
        datamart_modreport(a_conn)
    except:
        print("Could not complete Mod Reports!")
        m_conn.close()
        a_conn.close()
        return

    try:
        update_report_delta(a_conn)
    except:
        print("Could not update report delta!")
        m_conn.close()
        a_conn.close()
        return

    print("Successfully added Reports!")
    m_conn.close()
    a_conn.close()
    return



def main():
    etl_user()
    etl_listing()
    etl_report()

if __name__ == "__main__":
    main()