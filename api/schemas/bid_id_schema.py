from marshmallow import Schema, fields, validate


class BidIdSchema(Schema):
    """
    Schema for validating bid IDs.

    Attributes:
        bid_id (str): The bid ID to be validated.
    """

    bid_id = fields.Str(
        required=True, validate=validate.Length(min=36, error="Invalid bid Id")
    )
