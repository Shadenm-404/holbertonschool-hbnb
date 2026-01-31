#!/usr/bin/env bash
set -e

BASE_URL="http://127.0.0.1:80"
ADMIN_EMAIL="admin@hbnb.io"
ADMIN_PASSWORD="admin"

echo "BASE_URL=$BASE_URL"
echo
echo "============================================================"
echo
echo "### 0) Swagger page reachable"
echo
echo "============================================================"
curl -s -o /dev/null -w "HTTP %{http_code}\n" "$BASE_URL/api/v1/"
echo

extract_body() {
python3 - <<'PY'
import sys
raw = sys.stdin.read()

if "\r\n\r\n" in raw:
    body = raw.split("\r\n\r\n", 1)[1]
elif "\n\n" in raw:
    body = raw.split("\n\n", 1)[1]
else:
    body = raw

body = body.strip()

i1 = body.find("{")
i2 = body.find("[")
cands = [i for i in (i1, i2) if i != -1]
if cands:
    body = body[min(cands):]

print(body)
PY
}

json_get() {
python3 - <<'PY' "$1" "$2"
import json, sys
s = sys.argv[1].strip()
key = sys.argv[2]

i1 = s.find("{")
i2 = s.find("[")
cands = [i for i in (i1, i2) if i != -1]
if cands:
    s = s[min(cands):]

data = json.loads(s)
val = data.get(key, "")
if isinstance(val, (dict, list)):
    print(json.dumps(val))
else:
    print(val if val is not None else "")
PY
}

rand_email() {
  echo "user_$(uuidgen | cut -c1-8)@example.com"
}


echo
echo "============================================================"
echo
echo "### 1) Admin login (get JWT)"
echo
echo "============================================================"

LOGIN_RESP=$(curl -i -s -X POST "$BASE_URL/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$ADMIN_EMAIL\",\"password\":\"$ADMIN_PASSWORD\"}")

LOGIN_BODY=$(echo "$LOGIN_RESP" | extract_body)
TOKEN=$(json_get "$LOGIN_BODY" "access_token")

if [ -z "$TOKEN" ]; then
  echo "ERROR: token not returned"
  exit 1
fi

echo "$LOGIN_BODY"
echo
echo "OK: token captured (length: ${#TOKEN})"

AUTH_HEADER="Authorization: Bearer $TOKEN"


echo
echo "============================================================"
echo
echo "### 2) GET /users (admin protected)"
echo
echo "============================================================"

curl -i -s "$BASE_URL/api/v1/users/" \
  -H "$AUTH_HEADER"


echo
echo "============================================================"
echo
echo "### 3) POST /users (create normal user)"
echo
echo "============================================================"

USER_EMAIL=$(rand_email)

RESP=$(curl -i -s -X POST "$BASE_URL/api/v1/users/" \
  -H "$AUTH_HEADER" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$USER_EMAIL\",
    \"password\": \"123456\",
    \"first_name\": \"User\",
    \"last_name\": \"Test\"
  }")

USER_BODY=$(echo "$RESP" | extract_body)
USER_ID=$(json_get "$USER_BODY" "id")

echo "$USER_BODY"
echo
echo "OK: user_id=$USER_ID"


echo
echo "============================================================"
echo
echo "### 4) POST /amenities"
echo
echo "============================================================"

AMENITY_RESP=$(curl -i -s -X POST "$BASE_URL/api/v1/amenities/" \
  -H "$AUTH_HEADER" \
  -H "Content-Type: application/json" \
  -d '{"name":"WiFi"}')

AMENITY_BODY=$(echo "$AMENITY_RESP" | extract_body)
AMENITY_ID=$(json_get "$AMENITY_BODY" "id")

echo "$AMENITY_BODY"
echo
echo "OK: amenity_id=$AMENITY_ID"


echo
echo "============================================================"
echo
echo "### 5) POST /places"
echo
echo "============================================================"

PLACE_RESP=$(curl -i -s -X POST "$BASE_URL/api/v1/places/" \
  -H "$AUTH_HEADER" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Test Place\",
    \"description\": \"Nice place\",
    \"price\": 100,
    \"latitude\": 24.7,
    \"longitude\": 46.7,
    \"owner_id\": \"$USER_ID\",
    \"amenities\": [\"$AMENITY_ID\"]
  }")

PLACE_BODY=$(echo "$PLACE_RESP" | extract_body)
PLACE_ID=$(json_get "$PLACE_BODY" "id")

echo "$PLACE_BODY"
echo
echo "OK: place_id=$PLACE_ID"


echo
echo "============================================================"
echo
echo "### 6) POST /reviews"
echo
echo "============================================================"

REVIEW_RESP=$(curl -i -s -X POST "$BASE_URL/api/v1/reviews/" \
  -H "$AUTH_HEADER" \
  -H "Content-Type: application/json" \
  -d "{
    \"text\": \"Amazing place\",
    \"rating\": 5,
    \"user_id\": \"$USER_ID\",
    \"place_id\": \"$PLACE_ID\"
  }")

REVIEW_BODY=$(echo "$REVIEW_RESP" | extract_body)
REVIEW_ID=$(json_get "$REVIEW_BODY" "id")

echo "$REVIEW_BODY"
echo
echo "OK: review_id=$REVIEW_ID"


echo
echo "============================================================"
echo
echo "### 7) DELETE /reviews/{id}"
echo
echo "============================================================"

curl -i -s -X DELETE "$BASE_URL/api/v1/reviews/$REVIEW_ID" \
  -H "$AUTH_HEADER"
echo
echo "============================================================"
echo "ALL TESTS COMPLETED SUCCESSFULLY"
echo "============================================================"
