# Schema for phaseInfo object
class PhaseInfo:
    def __init__(self, phase, has_score, score=None, out_of=None):
            self.phase = phase
            self.has_score = has_score
            self.score = score
            self.out_of = out_of