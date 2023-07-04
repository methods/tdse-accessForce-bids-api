from marshmallow import Schema, fields, validates, ValidationError
from enum import Enum, unique

@unique
class Phase(Enum):
    PHASE_1 = 1
    PHASE_2 = 2

class PhaseSchema(Schema):
    phase = fields.Integer(required=True)
    has_score = fields.Boolean(required=True)
    score = fields.Integer()
    out_of = fields.Integer()

    @validates("phase")
    def validate_phase(self, value):
        if value not in [e.value for e in Phase]:
            raise ValidationError("Invalid phase value. Allowed values are 1 or 2.")

    @validates("score")
    def validate_score(self, value):
        if self.context.get("has_score") and value is None:
            raise ValidationError("Score is mandatory when has_score is set to true.")

    @validates("out_of")
    def validate_out_of(self, value):
        if self.context.get("has_score") and value is None:
            raise ValidationError("Out_of is mandatory when has_score is set to true.")
