# Schema for links object
class LinksModel:
    """
    Represents a links model for the bid resource.

    Attributes:
        self (str): The URL to the bid resource.
        questions (str): The URL to the questions resource related to the bid.
    """

    def __init__(self, bid_id):
        self.self = f"/bids/{bid_id}"
        self.questions = f"/bids/{bid_id}/questions"
