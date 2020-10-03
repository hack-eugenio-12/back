import requests

payload = "{ \"method\": \"testar\",  \"payload\": \"ON\",  \"timeout\": 10 }";
deviceId = "c7f78c4c-b27b-4164-aefe-b5b9d6486bf5"
headers = {
    'apikey': "Rv5BrH5A929jIGH5hX4HQoRDUM1CGugr",
    'content-type': "application/json"
    }

response = requests.request("POST", 'https://portal.stg.eugenio.io/api/v1/things/'+deviceId+'/invoke', data=payload, headers=headers)

print(response.text)
