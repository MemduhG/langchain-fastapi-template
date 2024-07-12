URL=localhost:8000/question
curl -X POST $URL -H "Content-Type: application/json" -d '{"input": "Why not trade with Sweden?", "detailed": false}'

echo

curl -X POST $URL -H "Content-Type: application/json" -d '{"input": "Who do I contact for info about sales restrictions?", "detailed": false}'

echo

curl -X POST $URL -H "Content-Type: application/json" -d '{"input": "Which countries are on our no sale list?", "detailed": false}'
