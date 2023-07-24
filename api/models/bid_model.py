from uuid import uuid4
from datetime import datetime
from api.models.status_enum import Status
from .links_model import LinksModel


# Description: Schema for the bid object
class BidModel:
    def __init__(
        self,
        tender,
        client,
        bid_date,
        alias=None,
        bid_folder_url=None,
        feedback=None,
        failed=None,
        was_successful=False,
        success=[],
        status=None,
        _id=None,
        links=None,
        last_updated=None,
    ):
        if _id is None:
            self._id = uuid4()
        else:
            self._id = _id
        if status is None:
            self.status = Status.IN_PROGRESS
        else:
            self.status = status
        self.tender = tender
        self.client = client
        self.alias = alias
        self.bid_date = bid_date
        self.bid_folder_url = bid_folder_url
        self.links = LinksModel(self._id)
        self.was_successful = was_successful
        self.success = success
        self.failed = failed
        self.feedback = feedback
        self.last_updated = datetime.now()
