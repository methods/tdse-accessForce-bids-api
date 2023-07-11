from marshmallow import Schema, fields, validate

class valid_bid_id_schema(Schema):
    bid_id = fields.UUID(required=True)