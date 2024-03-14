import os
import psycopg2

postgres_pass = os.environ["POSTGRES_PASSWORD"]

print ("hello world!")
print ("Welcome to python cron job")
print (postgres_pass)