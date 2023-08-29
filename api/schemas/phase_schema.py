"""
This module contains the schema for representing a bid phase.
"""
from enum import Enum, unique
from marshmallow import Schema, fields, validates_schema, ValidationError


@unique
class Phase(Enum):
    """
    Enum representing phases of a bid.

    Attributes:
        PHASE_1 (int): Phase 1 of the bid.
        PHASE_2 (int): Phase 2 of the bid.
    """

    PHASE_1 = 1
    PHASE_2 = 2


class PhaseSchema(Schema):
    """
    Schema for representing a bid phase.

    Attributes:
        phase (Phase): The phase of the bid.
        has_score (bool): Indicates if the phase has a score.
        score (int): The score of the phase (if applicable).
        out_of (int): The maximum score possible for the phase (if applicable).
    """

    phase = fields.Enum(Phase, required=True, by_value=True)
    has_score = fields.Boolean(required=True)
    score = fields.Integer()
    out_of = fields.Integer()

    @validates_schema
    def validate_score(self, data, **kwargs):
        if data["has_score"] is True and "score" not in data:
            raise ValidationError("Score is mandatory when has_score is set to true.")

    @validates_schema
    def validate_out_of(self, data, **kwargs):
        if data["has_score"] is True and "out_of" not in data:
            raise ValidationError("Out_of is mandatory when has_score is set to true.")
