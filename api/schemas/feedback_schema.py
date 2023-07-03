from marshmallow import Schema, fields

class FeedbackSchema(Schema):
    description = fields.Str(required=True)
    url = fields.Str(required=True)