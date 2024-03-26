#! /bin/bash
sleep 10
echo "Executing Grafana commands."
echo "Creating Grafana Owner user."

owner_pass=${DEFAULT_OWNER_PASSWORD}
postgres_pass=${POSTGRES_PASSWORD}

# checkuser=$(
# curl -X GET "http://kkadmin:${GF_SECURITY_ADMIN_PASSWORD}@grafana:3000/api/users/lookup?loginOrEmail=kkowner" \
#      -H "Accept: application/json" \
#      -H "Content-Type: application/json" \
# )


# Not doing an IF, simply because a bad init means the requirements are missing and there
# is no harm in doing another request.

curl -X POST \
  "http://kkadmin:${GF_SECURITY_ADMIN_PASSWORD}@grafana:3000/api/admin/users" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "kkowner",
    "login": "kkowner",
    "password": "'${DEFAULT_OWNER_PASSWORD}'"
}'

datasource=$(
curl -X POST \
  "http://kkadmin:${GF_SECURITY_ADMIN_PASSWORD}@grafana:3000/api/datasources" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
      "access": "proxy",
      "basicAuth": false,
      "basicAuthPassword": "",
      "basicAuthUser": "",
      "database": "analytics",
      "isDefault": true,
      "jsonData": {
          "postgresVersion": 1300,
          "sslmode": "disable"
      },
      "name": "postgres",
      "orgId": 1,
      "password": "",
      "readOnly": false,
      "user": "postgres",
      "secureJsonData": {
          "password": "'${POSTGRES_PASSWORD}'"
      },
      "type": "postgres",
      "url": "postgres:5432"
}'
)

uid=$(jq '.datasource.uid' <<< "${datasource}")

if [[ "$uid" == "null" ]]; then
  echo "Dashboard created already!"
else
  curl -X POST \
    "http://kkadmin:${GF_SECURITY_ADMIN_PASSWORD}@grafana:3000/api/dashboards/db" \
    -H "Accept: application/json" \
    -H "Content-Type: application/json" \
    -d @analytics.json #"$(cat analytics.json)"
fi


# if echo "$datasource" | jq -e 'has("uid")' > dev/null; then
#   uid="$datasource" | jq '.uid'
#   echo "$uid"
#   DS_POSTGRES=$uid envsubst < analytics.json
#   cat analytics.json
# else
#   echo "Already made the dashboard!"
# fi
# Create default data source and default dashboard(s).