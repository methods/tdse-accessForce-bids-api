from marshmallow import Schema, fields, post_load, validates, ValidationError
from datetime import datetime
from .links_schema import LinksSchema
from .phase_schema import PhaseSchema
from .feedback_schema import FeedbackSchema
from ..models.status_enum import Status


# Marshmallow schema
class UpdateBidSchema(Schema):
    _id = fields.UUID(required=True)
    tender = fields.Str(required=True)
    client = fields.Str(required=True)
    bid_date = fields.Date(required=True)
    alias = fields.Str()
    bid_folder_url = fields.Str()
    status = fields.Enum(Status, by_value=True, required=True)
    links = fields.Nested(LinksSchema, required=True)
    was_successful = fields.Bool(required=True)
    success = fields.List(fields.Nested(PhaseSchema))
    failed = fields.Nested(PhaseSchema)
    feedback = fields.Nested(FeedbackSchema)
    last_updated = fields.DateTime(required=True)

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

    @post_load
    def set_last_updated(self, data, **kwargs):
        data["last_updated"] = datetime.now().isoformat()
        return data
