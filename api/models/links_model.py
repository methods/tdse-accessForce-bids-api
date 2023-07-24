# Schema for links object
class LinksModel:
    def __init__(self, bid_id):
        self.self = f"/bids/{bid_id}"
        self.questions = f"/bids/{bid_id}/questions"
