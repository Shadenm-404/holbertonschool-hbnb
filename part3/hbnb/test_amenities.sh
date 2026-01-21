#!/bin/bash

echo "Starting HBnB server..."
python3 run.py &
SERVER_PID=$!
sleep 3

echo ""
echo "=============================="
echo "TEST 1: Create Amenity (POST)"
echo "=============================="

CREATE_RESPONSE=$(curl -s -X POST http://127.0.0.1:5000/api/v1/amenities/ \
-H "Content-Type: application/json" \
-d '{
  "name": "WiFi"
}')

echo "$CREATE_RESPONSE"

AMENITY_ID=$(echo "$CREATE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")

echo ""
echo "=============================="
echo "TEST 2: Get Amenity by ID (GET)"
echo "=============================="

curl -s http://127.0.0.1:5000/api/v1/amenities/$AMENITY_ID
echo ""

echo ""
echo "=============================="
echo "TEST 3: Update Amenity (PUT)"
echo "=============================="

curl -s -X PUT http://127.0.0.1:5000/api/v1/amenities/$AMENITY_ID \
-H "Content-Type: application/json" \
-d '{
  "name": "Updated WiFi"
}'
echo ""

echo ""
echo "=============================="
echo "TEST 4: Get All Amenities (GET)"
echo "=============================="

curl -s http://127.0.0.1:5000/api/v1/amenities/
echo ""

echo ""
echo "Stopping server..."
kill $SERVER_PID

