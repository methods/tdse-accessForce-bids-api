from marshmallow import Schema, fields, validate


class IdSchema(Schema):
    """
    Schema for validating path param IDs.

    Attributes:
        id (str): The bid ID to be validated.
    """

    id = fields.Str(
        required=True, validate=validate.Length(equal=36, error="Invalid Id")
    )
