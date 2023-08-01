from marshmallow import Schema, fields, post_load, validates_schema, ValidationError
from api.models.status_enum import Status
from api.models.bid_model import BidModel
from .bid_links_schema import BidLinksSchema
from .phase_schema import PhaseSchema
from .feedback_schema import FeedbackSchema


# Marshmallow schema for bid resource
class BidSchema(Schema):
    """
    Marshmallow schema for the bid object.

    Attributes:
        _id (UUID): The unique identifier of the bid.
        tender (str): The tender for which the bid is submitted.
        client (str): The client for whom the bid is prepared.
        bid_date (Date): The date when the bid was submitted (in the format "%Y-%m-%d").
        alias (str, optional): An alias or abbreviation for the client.
        bid_folder_url (str, optional): The URL to the bid's folder in the organization's SharePoint.
        was_successful (bool, optional): Whether the bid was successful or not.
        success (list of PhaseSchema, optional): A list of successful phases of the bid.
        failed (PhaseSchema, optional): The failed phase of the bid.
        feedback (FeedbackSchema, optional): Feedback information for the bid.
        status (Status): The status of the bid (using the Status enum).
        links (BidLinksSchema): Links to the bid resource and questions resource.
        last_updated (DateTime, optional): The date and time when the bid was last updated.
    """

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
    links = fields.Nested(BidLinksSchema)
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
