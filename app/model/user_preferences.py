from marshmallow import Schema, fields, post_load, validate
from app.model.news_topics import NewsTopics
from app.model.interest_levels import InterestLevels
from app.model.news_sources import NewsSource, NewsSourcesSchema
from app.model.topics import Topics, TopicsSchema
from app import db

class UserPreferences(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(50), nullable = False)
    user_email = db.Column(db.String(50), nullable = False)
    user_password = db.Column(db.String(50), nullable = False)
    age = db.Column(db.Integer, nullable = False)
    country = db.Column(db.String(20), nullable = False)
    time_to_read = db.Column(db.Integer)
    old_news_interest = db.Column(db.String(50))
    local_news_interest = db.Column(db.String(50))
    popular_tweets_interest = db.Column(db.String(50))

    def __init__(self, userCountry, userName, userEmail, userPassword, topicsRelatedToProfession, topicsRelatedToLeisure, timeToRead, age, oldNewsInterest, localNewsInterest, popularTweetsInterest, newsSourcePreferences):
        self.country = userCountry
        self.user_name = userName
        self.user_email = userEmail
        self.user_password = userPassword
        self.time_to_read = timeToRead
        self.age = age
        self.old_news_interest = oldNewsInterest
        self.local_news_interest = localNewsInterest
        self.popular_tweets_interest = popularTweetsInterest
        for topicProf in topicsRelatedToProfession:
            self.topics.append(Topics('Profession', topicProf['topicName'], topicProf['userInterestLevels']))
        for topicLeisure in topicsRelatedToLeisure:
            self.topics.append(Topics('Leisure', topicLeisure['topicName'], topicLeisure['userInterestLevels']))
        for newsSource in newsSourcePreferences:
            self.news_sources.append(NewsSource(newsSource['newsSourceName'], newsSource['userInterestLevels']))
        db.session.add(self)
        db.session.commit()

class UserPreferencesSchema(Schema):
    news_topics = [i.value for i in NewsTopics]
    general_preferences = [i.generalPreferences for i in InterestLevels]
    topic_preferences = [i.topicPreferences for i in InterestLevels]
    userCountry = fields.Str()
    userName = fields.Str()
    userEmail = fields.Email()
    userPassword = fields.Str()
    topicsRelatedToProfession = fields.List(fields.Nested(TopicsSchema))
    topicsRelatedToLeisure = fields.List(fields.Nested(TopicsSchema))
    timeToRead = fields.Int()
    age = fields.Int()
    oldNewsInterest = fields.Str(validate = validate.OneOf(general_preferences))
    localNewsInterest = fields.Str(validate = validate.OneOf(general_preferences))
    popularTweetsInterest = fields.Str(validate = validate.OneOf(general_preferences))
    newsSourcePreferences = fields.List(fields.Nested(NewsSourcesSchema))

    @post_load
    def create_user_preferences(self,data, **kwargs):
        return UserPreferences(**data).id
