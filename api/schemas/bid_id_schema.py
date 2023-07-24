from marshmallow import Schema, fields, validate


class BidIdSchema(Schema):
    bid_id = fields.Str(
        required=True, validate=validate.Length(min=36, error="Invalid bid Id")
    )
