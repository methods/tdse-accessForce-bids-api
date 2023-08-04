"""
This script is used to test the post and delete functionality of the API.
"""

import json
import requests


user_info = {"username": "Pira"}

response = requests.post(
    "http://localhost:5000/authorise/",
    data=json.dumps(user_info),
    headers={"Content-Type": "application/json"},
)

token = response.json()["jwt"]

# print(token)

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

# print(post_response)

bid_id = post_response.json()["_id"]

delete_url = f"http://localhost:8080/api/bids/{bid_id}"

delete_response = requests.delete(delete_url, headers=headers)

print(delete_response)
