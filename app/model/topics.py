from marshmallow import Schema, fields, post_load, validate
from app.model.interest_levels import InterestLevels
from app.model.news_topics import NewsTopics

from app import db

class Topics(db.Model):
    __tablename__ = 'topic_preferences'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    user = db.relationship('UserPreferences', backref = db.backref('topics', lazy = True))
    topic_type = db.Column(db.String, nullable = False)
    topic_name = db.Column(db.String, nullable = False)
    interest_level = db.Column(db.String, nullable = False)

    def __init__(self, topicType, topicName, interestLevel):
        self.topic_type = topicType
        self.topic_name = topicName
        self.interest_level = interestLevel

class TopicsSchema(Schema):
    interest_levels = [i.topicPreferences for i in InterestLevels]
    news_topics = [i.value for i in NewsTopics]
    topicName = fields.Str(validate = validate.OneOf(news_topics))
    userInterestLevels = fields.Str(validate = validate.OneOf(interest_levels))