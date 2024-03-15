import os
import psycopg2

DB_USER = "postgres"
DB_PASS = os.environ["POSTGRES_PASSWORD"]
DB_HOST = "postgres"
DB_PORT = "5432"

# def get_user_delta(m_conn, a_conn):
#     m_cursor = m_conn.cursor()

#     a_cursor = a_conn.cursor() 

#     m_cursor.execute("SELECT MAX(UserID) FROM kkuser")

#     main_max = m_cursor.fetchone()

#     a_cursor.execute("SELECT MAX(UserID) FROM core.delta")

#     analytics_max = a_cursor.fetchone()

#     return main_max[0], analytics_max[0]
    
# def extract_users(m_conn, a_delta):
#     m_cursor = m_conn.cursor()

#     m_cursor.execute('''
#                         SELECT 



#                      ''')


# def etl_user():
#     try:
#         m_conn = psycopg2.connect(database='main',
#                                     user=DB_USER,
#                                     password=DB_PASS,
#                                     host=DB_HOST,
#                                     port=DB_PORT)
        
#         a_conn = psycopg2.connect(database='analytics',
#                                         user=DB_USER,
#                                         password=DB_PASS,
#                                         host=DB_HOST,
#                                         port=DB_PORT)
#     except:
#         print("Couldn't connect to DB for extract_user")

#     deltas = get_user_delta(m_conn, a_conn)
#     m_delta = deltas[0]
#     a_delta = deltas[1]

#     if not m_delta or a_delta:
#         print("Could not retrieve deltas...")
#         m_conn.close()
#         a_conn.close()
#         return
    
#     if m_delta == a_delta:
#         print("No changes to Users!")
#         m_conn.close()
#         a_conn.close()
#         return

#     data = extract_users(m_conn, a_delta)

# SELECT  UserID,
# 		Email,
# 		FirstName,
# 		DateJoined,
# 		COALESCE(
# 			EXTRACT(year from l.DateJoined)*10000 
# 		  + EXTRACT('month' from l.DateJoined)*100
# 		  + EXTRACT('day' from l.DateJoined), 19000101) as DateJoinedFK,
# 		COALESCE( to_char(l.DateJoined, 'hh24mi'), '-1' ) AS TimeJoinedFK,
# 		UserRole,
# 		Verified,
# 		Blacklist,
# 		Politeness,
# 		Honesty,
# 		Quickness,
# 		NumReviews,


# SELECT u.UserID, COALESCE(mt.cnt + mf.cnt, 0) as NumMessages
# FROM kkuser u
# LEFT JOIN (SELECT MessageTo as UserID, COUNT(*) as cnt
# 		   FROM chat
# 		   GROUP BY MessageTo) mt ON u.UserID = mt.UserID
# LEFT JOIN (SELECT MessageFrom as UserID, COUNT(*) as cnt
# 		   FROM chat
# 		   GROUP BY MessageFrom) mf ON u.UserID = mf.UserID



def main():
    print("Hello World!")

if __name__ == "__main__":
    main()