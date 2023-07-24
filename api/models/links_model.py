# Schema for links object
class LinksModel:
    def __init__(self, id):
        self.self = f"/bids/{id}"
        self.questions = f"/bids/{id}/questions"
