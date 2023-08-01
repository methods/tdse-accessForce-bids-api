from marshmallow import Schema, fields


class BidLinksSchema(Schema):
    """
    Schema for representing links in a bid resource.

    Attributes:
        self (str): The URL to the bid resource.
        questions (str): The URL to the questions resource related to the bid.
    """

    self = fields.Str(required=True)
    questions = fields.Str(required=True)
