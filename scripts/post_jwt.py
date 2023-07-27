import json
import requests


user_info = {
    "username": "Tester McTestface",
    "admin": False,
    "write": True,
    "read": True,
}

response = requests.post(
    "http://localhost:5000/authorise/",
    data=json.dumps(user_info),
    headers={"Content-Type": "application/json"},
)

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IlRlc3RlciBNY1Rlc3RmYWNlIiwiYWRtaW4iOmZhbHNlLCJ3cml0ZSI6dHJ1ZSwicmVhZCI6dHJ1ZX0.EtqxvNchJ7t0R10JSQZIz7-ShhRdgRllAMgnSya3tOr"

print(token)

data = {
    "tender": "Business Intelligence and Data Warehousing",
    "client": "Office for National Statistics",
    "bid_date": "2023-06-23",
    "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
}

fstring = f"Bearer {token}"

headers = {"Content-Type": "application/json", "Authorization": fstring}

post_response = requests.post(
    "http://localhost:8080/api/bids", data=json.dumps(data), headers=headers
)

print(post_response)
