from newsapi import NewsApiClient
from app.business import cf_data
from app.model.news_article import NewsArticle
from app.business.news_rules_engine import NewsRuleEngine
from app.model.user_preferences import UserPreferences
from datetime import datetime, date
from typing import Dict
import pandas as pd
from pytrends.request import TrendReq

class ProcessNewsArticles:
    def __init__(self):
        self.__userProfilesDB = {}

    def calculateAgeOfNews(currentHeadlines):
        publishedAt = currentHeadlines["publishedAt"].split('T')[0]
        publishedYear = int(publishedAt.split('-')[0])
        publishedMonth = int(publishedAt.split('-')[1])
        publishedDate = int(publishedAt.split('-')[2])
        publishedFullDate = date(publishedYear, publishedMonth, publishedDate)
        today = datetime.utcnow().date()
        delta = today - publishedFullDate
        return delta.days

    def createNewsArticleObjects(headlines, topic_name, isLocalNews, isTrendingNews):
        articles = []
        for i in range(len(headlines)):
            currentHeadlines = headlines[i]
            daysOld = ProcessNewsArticles.calculateAgeOfNews(currentHeadlines)
            article = NewsArticle(i, currentHeadlines["url"], currentHeadlines["title"], currentHeadlines["description"], currentHeadlines["source"]["name"],
                                  topic_name, daysOld, isTrendingNews, isLocalNews)
            article.processArticle()
            articles.append(article)
        return articles

    def fetchTrendingStories():
        newsapi = NewsApiClient(api_key='7580ffe71bec47f7acfe7ea22d3520cc')
        articles=[]
        pytrend = TrendReq()
        df = pytrend.trending_searches()
        latestTrends = df[0].values.tolist()
        for trend in latestTrends[:5]:
            trending_news = newsapi.get_everything(q=trend,
                                                  page_size=1)
            articles.extend(ProcessNewsArticles.createNewsArticleObjects(trending_news["articles"], "Trending", False, True))
        return articles

    # download articles from websites base on user's profile
    def fetchNewsArticles(self, user_preferences: UserPreferences, aProcessArticles: bool = True) -> [NewsArticle]:
        # this is sample to download from one source
        articles = []
        newsapi = NewsApiClient(api_key='7580ffe71bec47f7acfe7ea22d3520cc')
        print(user_preferences.topics[0].topic_name)
        
        for index, topic in enumerate(user_preferences.topics):
            topic_name = topic.topic_name
            country = user_preferences.country
            topic_type = topic.topic_type
            if (topic_type == 'Profession'):
                top_headlines = newsapi.get_top_headlines(
                                                  category=topic_name.lower(),
                                                  country='us',
                                                  page_size=1)
                articles.extend(ProcessNewsArticles.createNewsArticleObjects(top_headlines["articles"], topic_name, False, False))
                top_local_headlines = newsapi.get_top_headlines(
                                                  category=topic_name.lower(),
                                                  q=country,
                                                  page_size=1)
                articles.extend(ProcessNewsArticles.createNewsArticleObjects(top_local_headlines["articles"], topic_name, True, False))

        articles.extend(ProcessNewsArticles.fetchTrendingStories())
        return articles

    def rankNewsArticles(self, aUserprofile: UserPreferences, aNewsArticles: [NewsArticle]) -> [str]:
        for i in range(len(aNewsArticles)):
            article = aNewsArticles[i]
            NewsRuleEngine.fireAllRules(aUserprofile, article)

        aNewsArticles.sort(key=lambda x: x.cf, reverse=True)

        articlesJson = []
        for i in range(len(aNewsArticles)): articlesJson.append(aNewsArticles[i].getJsonStr())

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