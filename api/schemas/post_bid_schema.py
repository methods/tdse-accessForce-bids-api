from marshmallow import Schema, fields, post_load, validates_schema, ValidationError
from api.models.bid_model import BidModel
from .links_schema import LinksSchema
from .phase_schema import PhaseSchema
from .feedback_schema import FeedbackSchema
from ..models.status_enum import Status


# Marshmallow schema for request body
class PostBidSchema(Schema):
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
    alias = fields.Str()
    bid_folder_url = fields.URL()
    was_successful = fields.Boolean()
    success = fields.List(fields.Nested(PhaseSchema))
    failed = fields.Nested(PhaseSchema)
    feedback = fields.Nested(FeedbackSchema)
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
