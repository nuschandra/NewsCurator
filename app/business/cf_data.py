from typing import Dict
from app.model.interest_levels import InterestLevels
from app.model.news_topics import NewsTopics

class Cf_Data:
    __topicPrefCf = {}
    __topicPrefCf[InterestLevels.STRONGLY_DISAGREE.topicPreferences] = -0.8
    __topicPrefCf[InterestLevels.DISAGREE.topicPreferences] = -0.4
    __topicPrefCf[InterestLevels.NOT_SURE.topicPreferences] = 0.0
    __topicPrefCf[InterestLevels.AGREE.topicPreferences] = 0.4
    __topicPrefCf[InterestLevels.STRONGLY_AGREE.topicPreferences] = 0.8

    __sourcePrefCf = {}
    __sourcePrefCf[InterestLevels.STRONGLY_DISAGREE.sourcePreferences] = -0.8
    __sourcePrefCf[InterestLevels.DISAGREE.sourcePreferences] = -0.4
    __sourcePrefCf[InterestLevels.NOT_SURE.sourcePreferences] = 0.0
    __sourcePrefCf[InterestLevels.AGREE.sourcePreferences] = 0.4
    __sourcePrefCf[InterestLevels.STRONGLY_AGREE.sourcePreferences] = 0.8
    
    __generalPrefCf = {}
    __generalPrefCf[InterestLevels.STRONGLY_DISAGREE.generalPreferences] = -0.8
    __generalPrefCf[InterestLevels.DISAGREE.generalPreferences] = -0.4
    __generalPrefCf[InterestLevels.NOT_SURE.generalPreferences] = 0.0
    __generalPrefCf[InterestLevels.AGREE.generalPreferences] = 0.4
    __generalPrefCf[InterestLevels.STRONGLY_AGREE.generalPreferences] = 0.8

    __readingTimeCf = {}
    __readingTimeCf[5] = {5: 0.8, 10: 0.6, 99: 0.2}
    __readingTimeCf[10] = {5: 0.6, 10: 0.8, 99: 0.6}
    __readingTimeCf[99] = {5: 0.0, 10: 0.0, 99: 0.0}

    __ageCf = {}
    __ageCf[29] = {NewsTopics.BUSINESS.name: 0.62, NewsTopics.TECHNOLOGY.name: 0.59, NewsTopics.SPORTS.name: 0.41, NewsTopics.SCIENCE.name: 0.59,
                   NewsTopics.HEALTH.name: 0.62, NewsTopics.ENTERTAINMENT.name: 0.58, NewsTopics.GENERAL.name: 0.57}
    __ageCf[39] = {NewsTopics.BUSINESS.name: 0.67, NewsTopics.TECHNOLOGY.name: 0.69, NewsTopics.SPORTS.name: 0.65, NewsTopics.SCIENCE.name: 0.69,
                   NewsTopics.HEALTH.name: 0.57, NewsTopics.ENTERTAINMENT.name: 0.46, NewsTopics.GENERAL.name: 0.79}
    __ageCf[59] = {NewsTopics.BUSINESS.name: 0.69, NewsTopics.TECHNOLOGY.name: 0.59, NewsTopics.SPORTS.name: 0.41, NewsTopics.SCIENCE.name: 0.59,
                   NewsTopics.HEALTH.name: 0.68, NewsTopics.ENTERTAINMENT.name: 0.28, NewsTopics.GENERAL.name: 0.73}
    __ageCf[99] = {NewsTopics.BUSINESS.name: 0.80, NewsTopics.TECHNOLOGY.name: 0.58, NewsTopics.SPORTS.name: 0.50, NewsTopics.SCIENCE.name: 0.58,
                   NewsTopics.HEALTH.name: 0.69, NewsTopics.ENTERTAINMENT.name: 0.31, NewsTopics.GENERAL.name: 0.79}

    def __init__(self): return

    @staticmethod
    def getTopicPrefCf(aTopicPref: str) -> float:
        cf = 0.0
        if(aTopicPref in Cf_Data.__topicPrefCf): cf = Cf_Data.__topicPrefCf[aTopicPref]
        return cf

    @staticmethod
    def getSourcePrefCf(aSourcePref: str) -> float: # aSourcePref = Enum SourcePref
        cf = 0.0
        if(aSourcePref in Cf_Data.__sourcePrefCf): cf = Cf_Data.__sourcePrefCf[aSourcePref]
        return cf

    @staticmethod
    def getGeneralPrefCf(aPreference: str) -> float:
        cf = 0.0
        if(aPreference in Cf_Data.__generalPrefCf): cf = Cf_Data.__generalPrefCf[aPreference]
        return cf

    @staticmethod
    def getReadingTimeCf(aPreferredReadingTime: float) -> Dict[int, float]: # return dict[reading time, cf]
        if (0 < aPreferredReadingTime <= 5):
            readingCf = Cf_Data.__readingTimeCf[5]
        elif (5 < aPreferredReadingTime <= 10):
            readingCf = Cf_Data.__readingTimeCf[10]
        else:
            readingCf = Cf_Data.__readingTimeCf[99]

        return readingCf

    @staticmethod
    def getAgeCf(aAge: int) -> Dict[str, float]:
        if (18 <= aAge <= 29):
            ageCf = Cf_Data.__ageCf[29]
        elif (29 < aAge <= 39):
            ageCf = Cf_Data.__ageCf[39]
        elif (39 < aAge <= 59):
            ageCf = Cf_Data.__ageCf[59]
        else:
            ageCf = Cf_Data.__ageCf[99]

        degradedAgeCf = {}
        keys = list(ageCf.keys())
        for key in keys: degradedAgeCf[key] = 0.2 * ageCf[key] # degrade cf taken from population survey
        return degradedAgeCf
