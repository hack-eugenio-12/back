curl -X POST https://portal.stg.eugenio.io/api/v1/things/c7f78c4c-b27b-4164-aefe-b5b9d6486bf5/invoke   -H 'apikey: Rv5BrH5A929jIGH5hX4HQoRDUM1CGugr'   -H 'Content-Type: application/json'   -d '{
  "method": "ligar",
  "payload": {
        "status": "LIGAR",
        "nivel": 50,
        "comando": "none"
    },
  "timeout": 30
}'
