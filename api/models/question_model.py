from uuid import uuid4
from datetime import datetime
from api.models.status_enum import Status


# Data model for question resource
class QuestionModel:
    def __init__(
        self,
        description,
        question_url,
        feedback,
        bid_id=None,
        response=None,
        score=None,
        out_of=None,
        respondents=[],
        status=None,
        links=None,
        last_updated=None,
        _id=None,
    ):
        if _id is None:
            self._id = uuid4()
        else:
            self._id = _id
        if status is None:
            self.status = Status.IN_PROGRESS
        else:
            self.status = status
        self.description = description
        self.question_url = question_url
        self.feedback = feedback
        self.response = response
        self.score = score
        self.out_of = out_of
        self.respondents = respondents
        if bid_id is None:
            self.links = links
        else:
            self.links = LinksModel(self._id, bid_id)

        self.last_updated = datetime.now()


# Model for links object
class LinksModel:
    """
    Represents a links model for the question resource.

    Attributes:
        self (str): The URL to the question resource.
        questions (str): The URL to the bid resource related to the question.
    """

    def __init__(self, question_id, bid_id):
        self.self = f"/api/bids/{bid_id}/questions/{question_id}"
        self.bid = f"/api/bids/{bid_id}"
