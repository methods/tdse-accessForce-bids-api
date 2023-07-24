from uuid import uuid4
from datetime import datetime
from api.models.status_enum import Status
from .links_model import LinksModel


# Description: Schema for the bid object
class BidModel:
    """
    Represents a bid model for the MongoDB database.

    Attributes:
        tender (str): The tender for which the bid is submitted.
        client (str): The client for whom the bid is prepared.
        bid_date (str): The date when the bid was submitted (in ISO format).
        alias (str): An alias or abbreviation for the client.
        bid_folder_url (str): The URL to the bid's folder in the organization's SharePoint.
        feedback (dict): A dictionary containing feedback information.
        success (list): A list of dictionaries representing successful phases of the bid.
        failed (dict): A dictionary representing the failed phase of the bid.
        links (dict): A dictionary containing links to the bid resource and questions resource.
        last_updated (str): The date and time when the bid was last updated (in ISO format).
    """

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
        success=None,
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
