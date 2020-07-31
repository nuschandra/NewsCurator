from marshmallow import Schema, fields, post_load, validate
from app.model.interest_levels import InterestLevels
from app import db

class NewsSource(db.Model):
    __tablename__ = 'news_source_preferences'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    user = db.relationship('UserPreferences', backref = db.backref('news_sources', lazy = True))
    source_name = db.Column(db.String, nullable = False)
    interest_level = db.Column(db.String, nullable = False)

    def __init__(self, sourceName, interestLevel):
        self.source_name = sourceName
        self.interest_level = interestLevel

class NewsSourcesSchema(Schema):
    interest_levels = [i.sourcePreferences for i in InterestLevels]
    newsSourceName = fields.Str()
    userInterestLevels = fields.Str(validate = validate.OneOf(interest_levels))