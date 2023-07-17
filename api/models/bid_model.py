from uuid import uuid4
from datetime import datetime
from .links_model import LinksModel
from api.models.status_enum import Status

# Description: Schema for the bid object
class BidModel():
    def __init__(self, tender, client, bid_date, alias=None, bid_folder_url=None, feedback=None, failed=None, was_successful=False, success=[], _id=uuid4(), status=Status.IN_PROGRESS):
        self._id = _id
        self.tender = tender
        self.client = client
        self.alias = alias
        self.bid_date = bid_date
        self.bid_folder_url = bid_folder_url
        self.status = status # enum: "deleted", "in_progress" or "completed"
        self.links = LinksModel(self._id)
        self.was_successful = was_successful
        self.success = success 
        self.failed = failed
        self.feedback = feedback
        self.last_updated = datetime.now()
