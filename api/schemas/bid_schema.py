# Description: Schema for the bid object
class BidSchema:
    def __init__(self, id, tender, client, bid_date, alias='', bid_folder_url='', status='in-progress', links=None, was_successful='', success=None, failed=None, feedback=None, last_updated=''):
        self.id = id
        self.tender = tender
        self.client = client
        self.alias = alias
        self.bid_date = bid_date
        self.bid_folder_url = bid_folder_url
        self.status = status # enum: "deleted", "in-progress" or "completed"
        self.links = links
        self.was_successful = was_successful
        self.success = success
        self.failed = failed
        self.feedback = feedback
        self.last_updated = last_updated

    def toDbCollection(self):
        return {
            "id": self.id,
            "tender": self.tender,
            "client": self.client,
            "alias": self.alias,
            "bid_date": self.bid_date,
            "bid_folder_url": self.bid_folder_url,
            "status": self.status, 
            "links": self.links,  
            "was_successful": self.was_successful,
            "success": self.success,
            "failed": self.failed,
            "feedback": self.feedback,
            "last_updated": self.last_updated
        }