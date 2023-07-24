from marshmallow import Schema, fields, post_load, validates_schema, ValidationError
from api.models.bid_model import BidModel
from .links_schema import LinksSchema
from .phase_schema import PhaseSchema
from .feedback_schema import FeedbackSchema
from ..models.status_enum import Status


# Marshmallow schema for request body
class BidSchema(Schema):
    _id = fields.UUID()
    tender = fields.Str(
        required=True,
        error_messages={"required": {"message": "Missing mandatory field"}},
    )
    client = fields.Str(
        required=True,
        error_messages={"required": {"message": "Missing mandatory field"}},
    )
    bid_date = fields.Date(
        format="%Y-%m-%d",
        required=True,
        error_messages={"required": {"message": "Missing mandatory field"}},
    )
    alias = fields.Str(allow_none=True)
    bid_folder_url = fields.URL(allow_none=True)
    was_successful = fields.Boolean(allow_none=True)
    success = fields.List(fields.Nested(PhaseSchema), allow_none=True)
    failed = fields.Nested(PhaseSchema, allow_none=True)
    feedback = fields.Nested(FeedbackSchema, allow_none=True)
    status = fields.Enum(Status, by_value=True)
    links = fields.Nested(LinksSchema)
    last_updated = fields.DateTime()

    @validates_schema
    def validate_unique_phases(self, data, **kwargs):
        # Get the list of success phases and the failed phase (if available)
        success_phases = data.get("success", [])
        failed_phase = data.get("failed", None)

        # Combine the success phases and the failed phase (if available)
        all_phases = success_phases + ([failed_phase] if failed_phase else [])

        # Extract phase values and remove any None values
        phase_values = [phase.get("phase") for phase in all_phases if phase]

        # Check if phase_values contain duplicates using sets
        if len(phase_values) != len(set(phase_values)):
            raise ValidationError("Phase values must be unique")

    # Creates a Bid instance after processing
    @post_load
    def makeBid(self, data, **kwargs):
        return BidModel(**data)
