from marshmallow import Schema, fields


class QuestionLinksSchema(Schema):
    """
    Schema for representing links in a question resource.

    Attributes:
        self (str): The URL to the question resource.
        questions (str): The URL to the bid resource related to the question.
    """

    self = fields.Str(required=True)
    bid = fields.Str(required=True)
