from marshmallow import Schema, fields, post_load
from .bid_schema import BidModel
from .links_schema import LinksSchema
from .phase_schema import PhaseSchema
from .feedback_schema import FeedbackSchema
from .status_enum import Status

# Marshmallow schema for request body
class BidRequestSchema(Schema):
    id = fields.UUID()
    tender = fields.Str(required=True, error_messages={"required": {"message": "Missing mandatory field"}})
    client = fields.Str(required=True, error_messages={"required": {"message": "Missing mandatory field"}})
    alias = fields.Str()
    bid_date = fields.Date(format='%d-%m-%Y', required=True, error_messages={"required": {"message": "Missing mandatory field"}})
    bid_folder_url = fields.URL()
    status = fields.Enum(Status, by_value=True)
    links = fields.Nested(LinksSchema)
    was_successful = fields.Bool()
    success = fields.List(fields.Nested(PhaseSchema))
    failed = fields.Nested(PhaseSchema)
    feedback = fields.Nested(FeedbackSchema)
    last_updated = fields.DateTime()

    # Creates a Bid instance after processing
    @post_load
    def makeBid(self, data, **kwargs):
        return BidModel(**data)