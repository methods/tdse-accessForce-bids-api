from marshmallow import Schema, fields, post_load
from datetime import datetime
from .links_schema import LinksSchema
from .phase_schema import PhaseSchema
from .feedback_schema import FeedbackSchema
from ..models.status_enum import Status


# Marshmallow schema
class BidSchema(Schema):
    _id = fields.UUID(required=True)
    tender = fields.Str(required=True)
    client = fields.Str(required=True)
    alias = fields.Str()
    bid_date = fields.Date(required=True)
    bid_folder_url = fields.Str()
    status = fields.Enum(Status, by_value=True, required=True)
    links = fields.Nested(LinksSchema, required=True)
    was_successful = fields.Bool(required=True)
    success = fields.List(fields.Nested(PhaseSchema))
    failed = fields.Nested(PhaseSchema)
    feedback = fields.Nested(FeedbackSchema)
    last_updated = fields.DateTime(required=True)

    @post_load
    def set_last_updated(self, data, **kwargs):
        data["last_updated"] = datetime.now().isoformat()
        return data
