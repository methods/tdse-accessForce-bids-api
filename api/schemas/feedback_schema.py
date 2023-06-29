from marshmallow import Schema, fields

# Schema for Feedback object
class Feedback:
    def __init__(self,description, url):
        self.description = description
        self.url = url

class FeedbackSchema(Schema):
    description = fields.Str(required=True)
    url = fields.Str(required=True)