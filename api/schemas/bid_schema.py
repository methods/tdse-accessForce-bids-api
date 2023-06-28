from uuid import uuid4
from datetime import datetime
from .phase_schema import PhaseInfo
from .status_schema import Status
from .feedback_schema import Feedback

# Description: Schema for the bid object
class BidSchema:
    def __init__(self, tender, client, bid_date, alias='', bid_folder_url='', feedback='', failed={}, was_successful=False, success=[]):
        self.id = uuid4()
        self.tender = tender
        self.client = client
        self.alias = alias
        self.bid_date = datetime.strptime(bid_date, '%d-%m-%Y').isoformat() # DD-MM-YYYY
        self.bid_folder_url = bid_folder_url
        self.status = Status.IN_PROGRESS.value # enum: "deleted", "in_progress" or "completed"
        self.links = {
            'self': f"/bids/{self.id}",
            'questions': f"/bids/{self.id}/questions"
        }
        self.was_successful = was_successful
        self.success = success 
        self.failed = failed
        self.feedback = feedback
        self.last_updated = datetime.now().isoformat()

    def addSuccessPhase(self, phase_info):
        self.success.append(phase_info)

    def setFailedPhase(self, phase_info):
        self.was_successful = False
        self.failed = phase_info

    def setStatus(self, status):
        if isinstance(status, Status):
            self.status = status.value
        else:
            raise ValueError("Invalid status. Please provide a valid Status enum value")
        
    def toDbCollection(self):
         self.success = [s.__dict__ for s in self.success] if self.success else []
         self.failed = self.failed.__dict__ if self.failed else None
         return self.__dict__

