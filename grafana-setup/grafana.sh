#! /bin/bash
sleep 5
echo "Executing Grafana commands."
echo "Creating Grafana Owner user."

owner_pass=${DEFAULT_OWNER_PASSWORD}

curl -X POST \
  "http://kkadmin:${GF_SECURITY_ADMIN_PASSWORD}@grafana:3000/api/admin/users" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "kkowner",
    "login": "kkowner",
    "password": "'${DEFAULT_OWNER_PASSWORD}'"
}'