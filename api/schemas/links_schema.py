from marshmallow import Schema, fields


class LinksSchema(Schema):
    self = fields.Str(required=True)
    questions = fields.Str(required=True)
