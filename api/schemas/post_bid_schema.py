from marshmallow import Schema, fields, post_load, validates, ValidationError
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context["failed_phase_values"] = set()

    @validates("success")
    def validate_success(self, value):
        phase_values = set()
        for phase in value:
            phase_value = phase.get("phase")
            if phase_value in phase_values:
                raise ValidationError(
                    "Phase value already exists in 'success' list and cannot be repeated."
                )
            phase_values.add(phase_value)

    @validates("failed")
    def validate_failed(self, value):
        phase_value = value.get("phase")
        if phase_value in self.context.get("success_phase_values", set()):
            raise ValidationError(
                "Phase value already exists in 'success' list and cannot be repeated."
            )
        self.context["failed_phase_values"].add(phase_value)

    @validates("success")
    def validate_success_and_failed(self, value):
        success_phase_values = set()
        failed_phase_values = self.context.get("failed_phase_values", set())
        for phase in value:
            phase_value = phase.get("phase")
            if phase_value in failed_phase_values:
                raise ValidationError(
                    "Phase value already exists in 'failed' section and cannot be repeated."
                )
            success_phase_values.add(phase_value)

    # Creates a Bid instance after processing
    @post_load
    def makeBid(self, data, **kwargs):
        return BidModel(**data)
