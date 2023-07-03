from marshmallow import Schema, fields

class PhaseSchema(Schema):
      phase = fields.Int(required=True, strict=True)
      has_score = fields.Bool(required=True)
      score = fields.Int(strict=True)
      out_of = fields.Int(strict=True)