import json
import requests

response = requests.get("http://localhost:5000/authorise/")

api_key = response.json()["API_KEY"]

print(api_key)

data = {
    "tender": "Business Intelligence and Data Warehousing",
    "client": "Office for National Statistics",
    "bid_date": "2023-06-23",
    "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
}

headers = {"Content-Type": "application/json", "X-API-Key": api_key}

post_response = requests.post(
    "http://localhost:8080/api/bids", data=json.dumps(data), headers=headers
)

print(post_response)
