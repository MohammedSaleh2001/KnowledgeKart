#! /bin/sh
psql -c '\set AUTOCOMMIT on'
psql -c "CREATE DATABASE main;"
psql -c "GRANT ALL PRIVILEGES ON DATABASE main TO postgres;"
psql -c "CREATE DATABASE analytics;"
psql -c "GRANT ALL PRIVILEGES ON DATABASE analytics TO postgres;"
psql -d analytics -c "CREATE SCHEMA core; CREATE SCHEMA datamart;"

for file in /etc/queries/main/*.sql;
do
    psql -d main -f "$file"
done

for file in /etc/queries/analytics/core/*.sql;
do
    psql -d analytics -f "$file"
done

for file in /etc/queries/analytics/datamart/*.sql;
do
    psql -d analytics -f "$file"
done

for file in /etc/queries/sample/*.sql;
do
    psql -d main -f "$file"
done
