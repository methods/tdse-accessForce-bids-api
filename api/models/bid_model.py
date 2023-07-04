from uuid import uuid4
from datetime import datetime
from .links_model import LinksModel
from api.models.status_enum import Status

# Description: Schema for the bid object
class BidModel():
    def __init__(self, tender, client, bid_date, alias=None, bid_folder_url=None, feedback=None, failed=None, was_successful=False, success=[]):
        self._id = uuid4()
        self.tender = tender
        self.client = client
        self.alias = alias
        self.bid_date = bid_date
        self.bid_folder_url = bid_folder_url
        self.status = Status.IN_PROGRESS # enum: "deleted", "in_progress" or "completed"
        self.links = LinksModel(self._id)
        self.was_successful = was_successful
        self.success = success 
        self.failed = failed
        self.feedback = feedback
        self.last_updated = datetime.now()


    def addSuccessPhase(self, phase):
        self.success.append(phase)

    def setFailedPhase(self, phase):
        self.was_successful = False
        self.failed = phase

    def addFeedback(self, feedback):
        self.feedback = feedback

    def setStatus(self, status):
        if isinstance(status, Status):
            self.status = status.value
        else:
            raise ValueError("Invalid status. Please provide a valid Status enum value")