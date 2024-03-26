import os
import psycopg2

DB_USER = "postgres"
DB_PASS = os.environ["POSTGRES_PASSWORD"]
DB_HOST = "postgres"
DB_PORT = "5432"

def get_user_delta(a_conn):

    a_cursor = a_conn.cursor() 

    a_cursor.execute("SELECT MAX(UserID) FROM core.delta")

    analytics_max = a_cursor.fetchone()

    return analytics_max[0]
    
def extract_transform_users(m_conn, a_delta):
    m_cursor = m_conn.cursor()

    # Note that UserID is last, since the update needs it in the last position
    m_cursor.execute(
            '''
            SELECT  u.Email,
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
                    (u.Honesty + u.Quickness + u.Politeness) / 3 as AvgUserRating,
                    u.UserID
                    
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
            WHERE u.UserID <= %s
            '''
        , (a_delta,))
    
    return m_cursor.fetchall()

def load_users(a_conn, data):
    a_cursor = a_conn.cursor()

    a_cursor.executemany(
        '''
        UPDATE core.kkuser SET (
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
        ) = (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
             %s, %s, %s, %s, %s, %s, %s, %s, %s)
        WHERE UserID = %s;
        '''
        , data
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

    a_delta = get_user_delta(a_conn)

    if a_delta is None:
        print("Could not retrieve update delta...")
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

    print("Successfully updated Users!")
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



def get_listing_delta(a_conn):

    a_cursor = a_conn.cursor() 

    a_cursor.execute("SELECT MAX(ListingID) FROM core.delta")

    analytics_max = a_cursor.fetchone()

    return analytics_max[0]
    
def extract_transform_listing(m_conn, a_delta):
    m_cursor = m_conn.cursor()

    m_cursor.execute(
            '''
            SELECT  l.UserID,
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
                    END as DifferenceAskingSoldPrice,
                    l.ListingID
            FROM listing l
            WHERE l.ListingID <= %s
            '''
        , (a_delta,))
    
    return m_cursor.fetchall()

def load_listing(a_conn, data):
    a_cursor = a_conn.cursor()

    # ON CONFLICT should never evaluate ideally
    a_cursor.executemany(
        '''
        UPDATE core.listing SET (
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
        ) = (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s)
        WHERE ListingID = %s;
        '''
        , data
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

    a_delta = get_listing_delta(a_conn)

    if a_delta is None:
        print("Could not retrieve update delta...")
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

    print("Successfully updated Listings!")
    m_conn.close()
    a_conn.close()
    return


def get_report_delta(a_conn):

    a_cursor = a_conn.cursor() 

    a_cursor.execute("SELECT MAX(ReportID) FROM core.delta")

    analytics_max = a_cursor.fetchone()

    return analytics_max[0]
    
def extract_transform_report(m_conn, a_delta):
    m_cursor = m_conn.cursor()

    m_cursor.execute(
            '''
            SELECT  r.ReportBy,
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
                    END as TimeToClose,
                    r.ReportID
            FROM report r
            WHERE r.ReportID <= %s
            '''
        , (a_delta,))
    
    return m_cursor.fetchall()

def load_report(a_conn, data):
    a_cursor = a_conn.cursor()

    # ON CONFLICT should never evaluate ideally
    a_cursor.executemany(
        '''
        UPDATE core.report SET (
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
        ) = (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s)
        WHERE ReportID = %s;
        '''
        , data
    )

    a_conn.commit()

    return True

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

    a_delta = get_report_delta(a_conn)

    if a_delta is None:
        print("Could not retrieve update delta...")
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

    print("Successfully updated Reports!")
    m_conn.close()
    a_conn.close()
    return



def main():
    etl_user()
    etl_listing()
    etl_report()

if __name__ == "__main__":
    main()