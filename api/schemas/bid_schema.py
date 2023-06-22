from uuid import uuid4
from datetime import datetime

# Description: Schema for the bid object
class BidSchema:
    def __init__(self, tender, client, bid_date, alias='', bid_folder_url='', status='in-progress', was_successful=False, failed=None, feedback=None):
        self.id = uuid4()
        self.tender = tender
        self.client = client
        self.alias = alias
        self.bid_date = datetime.strptime(bid_date, '%d-%m-%Y').isoformat() # DD-MM-YYYY
        self.bid_folder_url = bid_folder_url
        self.status = status # enum: "deleted", "in-progress" or "completed"
        self.links = {
            'self': f"/bids/{self.id}",
            'questions': f"/bids/{self.id}/questions"
        }
        self.was_successful = was_successful
        self.success = [] 
        self.failed = failed
        self.feedback = feedback
        self.last_updated = datetime.now().isoformat()

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
            "success": [s.__dict__ for s in self.success] if self.success else None,
            "failed": self.failed,
            "feedback": self.feedback,
            "last_updated": self.last_updated
        }
    
# Schema for phaseInfo object
class PhaseInfo:
    def __init__(self, phase, has_score, score=None, out_of=None):
            self.phase = phase
            self.has_score = has_score
            self.score = score
            self.out_of = out_of