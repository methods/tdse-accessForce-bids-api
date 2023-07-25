from marshmallow import Schema, fields


class FeedbackSchema(Schema):
    """
    Schema for the feedback data in a bid.

    Attributes:
        description (str): The description of the feedback.
        url (str): The URL of the feedback.
    """

    description = fields.Str(required=True)
    url = fields.URL(required=True)
