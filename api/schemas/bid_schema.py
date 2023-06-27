from uuid import uuid4
from datetime import datetime
from .phase_schema import PhaseInfo
from .status_schema import Status

# Description: Schema for the bid object
class BidSchema:
    def __init__(self, tender, client, bid_date, alias='', bid_folder_url='', status='in_progress', was_successful=True,success=[], failed={}, feedback_description=None, feedback_url=None):
        self.id = uuid4()
        self.tender = tender
        self.client = client
        self.alias = alias
        self.bid_date = datetime.strptime(bid_date, '%d-%m-%Y').isoformat() # DD-MM-YYYY
        self.bid_folder_url = bid_folder_url
        self.status = status # enum: "deleted", "in_progress" or "completed"
        self.links = {
            'self': f"/bids/{self.id}",
            'questions': f"/bids/{self.id}/questions"
        }
        self.was_successful = was_successful
        self.success = success 
        self.failed = failed
        self.feedback = {"description": feedback_description,
                         "url": feedback_url}
        self.last_updated = datetime.now().isoformat()

    def addSuccessPhase(self, phase, has_score, score=None, out_of=None):
        phase_info = PhaseInfo(phase=phase, has_score=has_score, score=score, out_of=out_of)
        self.success.append(phase_info)

    def setFailedPhase(self, phase, has_score, score=None, out_of=None):
         self.was_successful = False
         self.failed = PhaseInfo(phase=phase, has_score=has_score, score=score, out_of=out_of)

    def setStatus(self, status):
        if isinstance(status, Status):
            self.status = status.name.lower()
        else:
            raise ValueError("Invalid status. Please provide a valid Status enum value")

    def toDbCollection(self):
         self.success = [s.__dict__ for s in self.success] if self.success else []
         self.failed = self.failed.__dict__ if self.failed else {}
         return self.__dict__

