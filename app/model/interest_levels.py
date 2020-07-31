from enum import Enum

class InterestLevels(Enum):
    STRONGLY_DISAGREE = ("Not Related", "Exclude", "Definitely Not")
    DISAGREE = ("Unlikely to be related", "Prefer to exclude", "Not really")
    NOT_SURE = ("Not sure", "No preference", "No preference")
    AGREE = ("Likely to be related", "Prefer to include", "I suppose")
    STRONGLY_AGREE = ("Strongly related", "Include", "Definitely")

    def __init__(self, topicPreferences, sourcePreferences, generalPreferences):
        self.topicPreferences = topicPreferences
        self.sourcePreferences = sourcePreferences
        self.generalPreferences = generalPreferences