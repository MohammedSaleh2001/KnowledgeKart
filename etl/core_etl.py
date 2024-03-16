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
                                    (SELECT MAX(UserReportDate) 
                                    FROM datamart.userreport), '2024-03-10'::TIMESTAMP 
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


def main():
    etl_user()

if __name__ == "__main__":
    main()