from marshmallow import Schema, fields, post_load
from api.models.status_enum import Status
from api.models.question_model import QuestionModel
from .question_links_schema import QuestionLinksSchema
from .feedback_schema import FeedbackSchema


# Marshmallow schema for question resource
class QuestionSchema(Schema):
    _id = fields.UUID()
    description = fields.Str(
        required=True,
        error_messages={"required": {"message": "Missing mandatory field"}},
    )
    question_url = fields.URL(
        required=True,
        error_messages={"required": {"message": "Missing mandatory field"}},
    )
    feedback = fields.Nested(
        FeedbackSchema,
        required=True,
        error_messages={"required": {"message": "Missing mandatory field"}},
    )
    bid_id = fields.UUID(required=True)
    response = fields.Str()
    score = fields.Integer()
    out_of = fields.Integer()
    respondents = fields.List(fields.Str())
    status = fields.Enum(Status, by_value=True)
    links = fields.Nested(QuestionLinksSchema)
    last_updated = fields.DateTime()

    # Creates a Question instance after processing
    @post_load
    def makeQuestion(self, data, **kwargs):
        return QuestionModel(**data)
