from marshmallow import Schema, fields

# Schema for phaseInfo object
class Phase:
    def __init__(self, phase, has_score, score=None, out_of=None):
            self.phase = phase
            self.has_score = has_score
            self.score = score
            self.out_of = out_of

class PhaseSchema(Schema):
      phase = fields.Int(required=True)
      has_score = fields.Bool(required=True)
      score = fields.Int()
      out_of = fields.Int()