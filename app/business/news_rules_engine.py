from app.model.user_preferences import UserPreferences
from app.model.news_article import NewsArticle
from app.model.topics import Topics
from app.model.news_sources import NewsSource
from app.business.cf_data import Cf_Data
from app import db

class NewsRuleEngine:
    def __init__(self): return

    @staticmethod
    def fireAllRules(aUserProfile: UserPreferences, aNewsArticle: NewsArticle, aArticleType: str = 'Profession') -> int:
        rulesFired = 0

        if aArticleType=='Profession':
            if (NewsRuleEngine.ruleWorkTopic(aUserProfile, aNewsArticle)): rulesFired += 1
        elif aArticleType == 'Leisure':
            if (NewsRuleEngine.ruleLeisureTopic(aUserProfile, aNewsArticle)): rulesFired += 1
        if (NewsRuleEngine.ruleReadingTime(aUserProfile, aNewsArticle)): rulesFired += 1
        if (NewsRuleEngine.ruleAgePref(aUserProfile, aNewsArticle)): rulesFired += 1
        if (NewsRuleEngine.ruleSeePastNews(aUserProfile, aNewsArticle)): rulesFired += 1
        if (NewsRuleEngine.ruleSeeLocalNews(aUserProfile, aNewsArticle)): rulesFired += 1
        if (NewsRuleEngine.ruleSeeTrendingNews(aUserProfile, aNewsArticle)): rulesFired += 1
        if (NewsRuleEngine.ruleNewsSource(aUserProfile, aNewsArticle)): rulesFired += 1

        return rulesFired

    @staticmethod
    def ruleWorkTopic(aUserProfile: UserPreferences, aNewsArticle: NewsArticle) -> bool:
        fired=False
        topic = aNewsArticle.topic
        user_id = aUserProfile.id
        topic_from_db = Topics.query.filter_by(user_id=user_id, topic_name=topic, topic_type='Profession').first()
        if topic_from_db is not None:
            user_interest_level = topic_from_db.interest_level
            print(user_interest_level)
            aNewsArticle.updateCf(Cf_Data.getTopicPrefCf(user_interest_level))
            fired=True
        
        print("Fired value for is:", topic, fired)
        return fired

    @staticmethod
    def ruleLeisureTopic(aUserProfile: UserPreferences, aNewsArticle: NewsArticle) -> bool:
        topic = aNewsArticle.topic
        fired = False
        user_id = aUserProfile.id
        topic_from_db = Topics.query.filter_by(user_id=user_id, topic_name=topic, topic_type='Leisure').first()
        if topic_from_db is not None:
            user_interest_level = topic_from_db.interest_level
            print(user_interest_level)
            aNewsArticle.updateCf(Cf_Data.getTopicPrefCf(user_interest_level))
            fired=True
            
        return fired

    @staticmethod
    def ruleReadingTime(aUserProfile: UserPreferences, aNewsArticle: NewsArticle) -> bool:
        user_readingTime = aUserProfile.time_to_read
        readingTimeCf = Cf_Data.getReadingTimeCf(user_readingTime)

        if (0 < aNewsArticle.readingTime <= 5):
            cf = readingTimeCf[5]
        elif (5 < aNewsArticle.readingTime <= 10):
            cf = readingTimeCf[10]
        else:
            cf = readingTimeCf[99]

        aNewsArticle.updateCf(cf)

        return True

    @staticmethod
    def ruleAgePref(aUserProfile: UserPreferences, aNewsArticle: NewsArticle) -> bool:
        topic = aNewsArticle.topic.upper()
        cf = 0.0
        agePrefCf = Cf_Data.getAgeCf(aUserProfile.age)
        if(topic.upper() in agePrefCf):
            cf = agePrefCf[topic]

        aNewsArticle.updateCf(cf)
        return True

    @staticmethod
    def ruleSeePastNews(aUserProfile: UserPreferences, aNewsArticle: NewsArticle) -> bool:
        isPastNews = (aNewsArticle.date > 1) # more than 1-day old article
        if isPastNews:
            aNewsArticle.updateCf(Cf_Data.getGeneralPrefCf(aUserProfile.old_news_interest))
            fired = True
        else:
            fired = False

        return fired

    @staticmethod
    def ruleSeeLocalNews(aUserProfile: UserPreferences, aNewsArticle: NewsArticle) -> bool:
        if aNewsArticle.isLocalNews:
            aNewsArticle.updateCf(Cf_Data.getGeneralPrefCf(aUserProfile.local_news_interest))
            fired = True
        else:
            fired = False

        return fired

    @staticmethod
    def ruleSeeTrendingNews(aUserProfile: UserPreferences, aNewsArticle: NewsArticle) -> bool:
        if aNewsArticle.isTrending:
            aNewsArticle.updateCf(Cf_Data.getGeneralPrefCf(aUserProfile.popular_tweets_interest))
            fired = True
        else:
            fired = False

        return fired

    @staticmethod
    def ruleNewsSource(aUserProfile: UserPreferences, aNewsArticle: NewsArticle) -> bool:
        source = aNewsArticle.source
        user_id = aUserProfile.id
        source_from_db = NewsSource.query.filter_by(user_id=user_id, source_name=source).first()
        if (source_from_db is not None):
            fired = True
            user_interest_level = source_from_db.interest_level
            aNewsArticle.updateCf(Cf_Data.getSourcePrefCf(user_interest_level))
        else:
            fired = False

        return fired