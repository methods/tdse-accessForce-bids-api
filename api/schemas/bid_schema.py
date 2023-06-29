from uuid import uuid4
from datetime import datetime
from marshmallow import Schema, fields
from .links_schema import Links, LinksSchema
from .phase_schema import Phase, PhaseSchema
from .feedback_schema import Feedback, FeedbackSchema
from .status_enum import Status

# Description: Schema for the bid object
class Bid():
    def __init__(self, tender, client, bid_date, alias=None, bid_folder_url=None, feedback=None, failed=None, was_successful=False, success=[]):
        self.id = uuid4()
        self.tender = tender
        self.client = client
        self.alias = alias
        self.bid_date = datetime.strptime(bid_date, '%d-%m-%Y').isoformat() # DD-MM-YYYY
        self.bid_folder_url = bid_folder_url
        self.status = Status.IN_PROGRESS # enum: "deleted", "in_progress" or "completed"
        self.links = Links(self.id)
        self.was_successful = was_successful
        self.success = success 
        self.failed = failed
        self.feedback = feedback
        self.last_updated = datetime.now().isoformat()

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

# Marshmallow schema
class BidSchema(Schema):
    id = fields.Str(required=True)
    tender = fields.Str(required=True)
    client = fields.Str(required=True)
    alias = fields.Str()
    bid_date = fields.Str(required=True)
    bid_folder_url = fields.Str()
    status = fields.Enum(Status, required=True)
    links = fields.Nested(LinksSchema, required=True)
    was_successful = fields.Bool(required=True)
    success = fields.List(fields.Nested(PhaseSchema))
    failed = fields.Nested(PhaseSchema)
    feedback = fields.Nested(FeedbackSchema)
    last_updated = fields.Str(required=True)