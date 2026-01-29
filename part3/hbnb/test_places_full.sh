#!/usr/bin/env bash

set -e

BASE_URL="http://127.0.0.1:5000/api/v1"

echo "=============================="
echo " PLACES FULL TEST STARTED"
echo "=============================="

# ------------------------------
# LOGIN ADMIN
# ------------------------------
ADMIN_LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hbnb.io","password":"admin1234"}')

ADMIN_TOKEN=$(python3 - <<EOF
import json
print(json.loads("""$ADMIN_LOGIN""")["access_token"])
EOF
)

AUTH_ADMIN="Authorization: Bearer $ADMIN_TOKEN"

# ------------------------------
# CREATE USER (PLACE OWNER)
# ------------------------------
OWNER_EMAIL="place_owner_$(date +%s)@example.com"

curl -s -X POST $BASE_URL/users/ \
  -H "Content-Type: application/json" \
  -H "$AUTH_ADMIN" \
  -d "{
    \"email\": \"$OWNER_EMAIL\",
    \"password\": \"owner123\",
    \"first_name\": \"Place\",
    \"last_name\": \"Owner\"
  }" > /dev/null

# ------------------------------
# LOGIN OWNER
# ------------------------------
OWNER_LOGIN=$(curl -s -X POST $BASE_URL/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$OWNER_EMAIL\",\"password\":\"owner123\"}")

OWNER_TOKEN=$(python3 - <<EOF
import json
print(json.loads("""$OWNER_LOGIN""")["access_token"])
EOF
)

AUTH_OWNER="Authorization: Bearer $OWNER_TOKEN"

# ------------------------------
# CREATE PLACE
# ------------------------------
echo "== CREATE PLACE =="

PLACE=$(curl -s -X POST $BASE_URL/places/ \
  -H "Content-Type: application/json" \
  -H "$AUTH_OWNER" \
  -d '{
    "title": "Test Place",
    "description": "Place created for testing",
    "price_per_night": 150
  }')

echo "$PLACE"

PLACE_ID=$(python3 - <<EOF
import json
print(json.loads("""$PLACE""")["id"])
EOF
)

# ------------------------------
# GET PLACE
# ------------------------------
echo "== GET PLACE =="

curl -s -X GET $BASE_URL/places/$PLACE_ID

# ------------------------------
# UPDATE PLACE
# ------------------------------
echo "== UPDATE PLACE =="

curl -s -X PUT $BASE_URL/places/$PLACE_ID \
  -H "Content-Type: application/json" \
  -H "$AUTH_OWNER" \
  -d '{
    "price_per_night": 200
  }'

# ------------------------------
# DELETE PLACE
# ------------------------------
echo "== DELETE PLACE =="

curl -s -X DELETE $BASE_URL/places/$PLACE_ID \
  -H "$AUTH_OWNER"

# ------------------------------
# GET PLACE AFTER DELETE
# ------------------------------
echo "== GET PLACE AFTER DELETE =="

curl -s -X GET $BASE_URL/places/$PLACE_ID

echo ""
echo "=============================="
echo " PLACES FULL TEST COMPLETED"
echo "=============================="
