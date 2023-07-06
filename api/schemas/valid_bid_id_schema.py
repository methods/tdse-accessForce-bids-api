from marshmallow import Schema, fields, validate

class valid_bid_id_schema(Schema):
    bid_id = fields.UUID(validate=validate.Length(min=1), error_messages={"validate": "Invalid Bid ID"})