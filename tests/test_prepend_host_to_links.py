from helpers.helpers import prepend_host_to_links

def test_prepend_host():
    resource = {
      "_id": "9f688442-b535-4683-ae1a-a64c1a3b8616",
      "alias": "ONS",
      "bid_date": "2023-06-23",
      "bid_folder_url": "https://organisation.sharepoint.com/Docs/dummyfolder",
      "client": "Office for National Statistics",
      "last_updated": "2023-07-19T11:15:25.743340",
      "links": {
        "questions": "/bids/9f688442-b535-4683-ae1a-a64c1a3b8616/questions",
        "self": "/bids/9f688442-b535-4683-ae1a-a64c1a3b8616"
      },
      "status": "in_progress",
      "tender": "Business Intelligence and Data Warehousing",
      "was_successful": False
    }
    hostname = "localhost:8080"
    
    result = prepend_host_to_links(resource, hostname)

    assert result["links"] == {
        "questions": "http://localhost:8080/bids/9f688442-b535-4683-ae1a-a64c1a3b8616/questions",
        "self": "http://localhost:8080/bids/9f688442-b535-4683-ae1a-a64c1a3b8616"
      }