from newsapi import NewsApiClient
from newsapi.newsapi_exception import NewsAPIException
from app.model.news_article import NewsArticle
from app.business.news_rules_engine import NewsRuleEngine
from app.business.keyword_matcher import KeywordMatcher
from app.model.news_topics import NewsTopics
from app.model.user_preferences import UserPreferences
from app.model.interest_levels import InterestLevels
from app.model.countries import Countries
from datetime import datetime, date
from typing import Dict
from pytrends.request import TrendReq
import random
import math

class ProcessNewsArticles:
    def __init__(self):
        self.__userProfilesDB = {}
        self.__keywordMatcher = None
        self.__newsapiKey = 'fd9342e6dd8e4a0b97bab8e760382743' #'7580ffe71bec47f7acfe7ea22d3520cc'
        self.__trendingArticles = []

    def calculateAgeOfNews(self, currentHeadlines):
        publishedAt = currentHeadlines["publishedAt"].split('T')[0]
        publishedYear = int(publishedAt.split('-')[0])
        publishedMonth = int(publishedAt.split('-')[1])
        publishedDate = int(publishedAt.split('-')[2])
        publishedFullDate = date(publishedYear, publishedMonth, publishedDate)
        today = datetime.utcnow().date()
        delta = today - publishedFullDate
        return delta.days
    
    def checkIfTrending(self, article):
        articleKeywords = article.keywords
        for index, trend in enumerate(self.__trendingArticles):
            isTrending = self.__keywordMatcher.trendingNewsScore(trend.keywords, articleKeywords)
            if (isTrending):
                return True

        return False

    def createNewsArticleObjects(self, headlines, topic_name):
        articles = []
        for i in range(len(headlines)):
            currentHeadlines = headlines[i]
            daysOld = self.calculateAgeOfNews(currentHeadlines)
            article = NewsArticle(i, currentHeadlines["url"], currentHeadlines["title"], currentHeadlines["description"], currentHeadlines["source"]["name"],
                                  topic_name, daysOld, False, False, currentHeadlines["content"])

            # shifted processArticle() to rankNewsArticles() so that only the top 10 articles will be
            # downloaded, this improves speed but its traded off with articles tagged using truncated content
            # ---------------------------------------------------------------------------------------
            article.processArticle()
            # ---------------------------------------------------------------------------------------

            matchScore = self.__keywordMatcher.computeMatchingScore(article.content)
            article.isLocalNews = (matchScore > 0.002)
            article.isTrending = self.checkIfTrending(article)
            articles.append(article)
        return articles

    def getTrendingArticles(self, keywd_matcher: KeywordMatcher):
        newsapi = NewsApiClient(api_key = self.__newsapiKey )
        pytrend = TrendReq()
        df = pytrend.trending_searches()
        latestTrends = df[0].values.tolist()
        trendingArticles = []
        try:
            for trend in latestTrends[:5]:
                trending_news = newsapi.get_everything(q=trend, page_size=1)
                trending_headline = trending_news["articles"][0]  # since we are getting only one article for each trend
                daysold = self.calculateAgeOfNews(trending_headline)
                trending_headline_object = NewsArticle(0, trending_headline["url"], trending_headline["title"],
                                                       trending_headline["description"],
                                                       trending_headline["source"]["name"],
                                                       "Trending", daysold, True, False, trending_headline["content"])
                trending_headline_object.processArticle()

                # call labeller for local news
                matchScore = self.__keywordMatcher.computeMatchingScore(trending_headline_object.content)
                trending_headline_object.isLocalNews = (matchScore > 0.002)

                trendingArticles.append(trending_headline_object)
        except (ValueError, TypeError, NewsAPIException) as e:
            content = e.args[0] if isinstance(e, ValueError) or isinstance(e, TypeError) else e.get_message()
            article = NewsArticle(0, "", "API Error", "Error", "NewsAPI", NewsTopics.GENERAL.name, 0, False, False)
            article.keywords = [content]
            trendingArticles.append(article)

        return trendingArticles

    def getTopicDistribution(self, user_preferences: UserPreferences, article_type: str):
        distribution = {}
        for topic in user_preferences.topics:
            if topic.topic_type == article_type:
                topic_interest = topic.interest_level
                if topic_interest == InterestLevels.AGREE.topicPreferences or topic_interest == InterestLevels.STRONGLY_AGREE.topicPreferences:
                    distribution[topic.topic_name] = 2
                elif topic_interest == InterestLevels.NOT_SURE.topicPreferences or topic_interest == InterestLevels.DISAGREE.topicPreferences:
                    distribution[topic.topic_name] = 1
                else:
                    distribution[topic.topic_name] = 0

        sumtotal = sum(distribution.values())
        for key in distribution.keys():
            if distribution[key] == 2:
                distribution[key] = int(math.ceil((distribution[key] / sumtotal) * 10)) if sumtotal > 0 else 0
            else:
                distribution[key] = int(math.floor((distribution[key] / sumtotal) * 10)) if sumtotal > 0 else 0

        return distribution

    def removeDuplicatedHeadlines(self, headlines, currentArticles: [NewsArticle]):
        for i in range(len(headlines)-1, -1, -1): # remove duplicated articles
            headline = headlines[i]
            for article in currentArticles:
                if article.title == headline['title']:
                    headlines.remove(headline)
                    break
        return headlines

    # download articles from websites base on user's profile
    def fetchNewsArticles(self, user_preferences: UserPreferences, article_type: str = 'Profession', aProcessArticles: bool = True) -> [NewsArticle]:
        country = user_preferences.country
        self.__keywordMatcher = KeywordMatcher(Countries.getCountries()[user_preferences.country])
        self.__trendingArticles = self.getTrendingArticles(self.__keywordMatcher)
        newsapi = NewsApiClient(api_key=self.__newsapiKey)
        # print(user_preferences.topics[0].topic_name)
        topicDistri = self.getTopicDistribution(user_preferences, article_type)
        try:
            articles = []
            for index, topic in enumerate(random.sample(user_preferences.topics, len(user_preferences.topics))):
                if len(articles) >= 20: break
                topic_name = topic.topic_name
                pg_size = topicDistri[topic_name]
                if country == 'us': pg_size = 2 * pg_size
                if topic.topic_type == article_type and pg_size > 0:
                    top_headlines = newsapi.get_top_headlines(category=topic_name.lower(),
                                                              country='us',
                                                              page_size=pg_size)
                    articles.extend(self.createNewsArticleObjects(top_headlines["articles"], topic_name))

                    if country != 'us':
                        top_local_headlines = newsapi.get_top_headlines(category=topic_name.lower(),
                                                                        country=country,
                                                                        page_size=pg_size)
                        self.removeDuplicatedHeadlines(top_local_headlines["articles"], articles)
                        articles.extend(self.createNewsArticleObjects(top_local_headlines["articles"], topic_name))

            articles.extend(self.__trendingArticles)
        except (ValueError, TypeError, NewsAPIException) as e:
            content = e.args[0] if isinstance(e, ValueError) or isinstance(e, TypeError) else e.get_message()
            article = NewsArticle(0, "", "API Error", "Error", "NewsAPI", NewsTopics.GENERAL.name, 0, False, False)
            article.keywords = [content]
            articles = [article]
        return articles

    def rankNewsArticles(self, aUserprofile: UserPreferences, aNewsArticles: [NewsArticle], aArticleType: str = 'Profession') -> [str]:
        for i in range(len(aNewsArticles)):
            article = aNewsArticles[i]
            NewsRuleEngine.fireAllRules(aUserprofile, article, aArticleType)

        aNewsArticles.sort(key=lambda x: x.cf, reverse=True)

        articlesJson = []
        for i in range(0, min(10, len(aNewsArticles))):
            #aNewsArticles[i].processArticle()
            articlesJson.append(aNewsArticles[i].getJsonStr())

        return articlesJson

    def getUserprofile(self, aUserId: int) -> UserPreferences:
        return self.__userProfilesDB[aUserId]

    def getFirstProfile(self) -> UserPreferences:

        if len(self.__userProfilesDB) > 0:
            userprofile = self.__userProfilesDB[next(iter(self.__userProfilesDB))]
        else:
            userprofile = None

        return userprofile

    @property
    def userprofileDB(self) -> Dict[int, UserPreferences]: return self.__userProfilesDB