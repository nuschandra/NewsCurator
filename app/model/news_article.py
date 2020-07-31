from newspaper import Article
from app.business.utils import EnumEncoder
import json

class NewsArticle:
    def __init__(self, aID: int, aUrl: str, aTitle: str, aDesc: str, aSource: str, aTopic, aDate: int, aIsTrending: bool, aIsLocalNews: bool,
                 aLength: int = 1):
        self.__id = int(aID)
        self.__title = str(aTitle)
        self.__url = str(aUrl)
        self.__description = str(aDesc)
        self.__source = str(aSource)
        self.__topic = str(aTopic)
        self.__date = int(aDate) # no. of days ago this article was published; 0 = today, 1 = yesterday, 2 = the day before, ...
        self.__isTreading = bool(aIsTrending)
        self.__isLocalNews = bool(aIsLocalNews)

        self.__readingSpeed = 250.0  # average reading time is 200 - 300 words per min
        self.__articleProcessed = False
        self.content = "NewsContent"
        self.length = aLength
        self.__keywords = []
        self.__summary = ""
        self.__cf = 0.0


    # getter and setters
    @property
    def id(self) -> int: return self.__id

    @property
    def title(self) -> str: return self.__title

    @property
    def url(self) -> str: return self.__url

    @property
    def description(self) -> str: return self.__description

    @property
    def length(self) -> int: return self.__length

    @length.setter
    def length(self, aValue: int):
        self.__length = aValue
        self.__readingTime_min = float(self.__length) / self.__readingSpeed

    @property
    def readingTime(self) -> float: return self.__readingTime_min

    @property
    def source(self) -> str: return self.__source

    @property
    def topic(self) -> str: return self.__topic

    @property
    def date(self) -> int: return self.__date

    @property
    def isTrending(self) -> bool: return self.__isTreading

    @property
    def isLocalNews(self) -> bool: return self.__isLocalNews

    @property
    def cf(self) -> float: return self.__cf

    @property
    def content(self) -> str: return self.__content

    @content.setter
    def content(self, aValue: str):
        self.__content = aValue
        if len(self.__content) > 0:
            self.__length = len(self.__content.split(' '))
            self.__readingTime_min = float(self.__length) / self.__readingSpeed

    @property
    def keywords(self) -> []: return self.__keywords

    @keywords.setter
    def keywords(self, aValue: []): self.__keywords = aValue

    @property
    def summary(self) -> str: return self.__summary

    @summary.setter
    def summary(self, aValue: str): self.__keywords = aValue



    def getJsonStr(self) -> str:
        jsonstr = json.dumps(self.__dict__, cls=EnumEncoder)
        jsonstr = jsonstr.replace("_" + self.__class__.__name__ + "__", "")
        return jsonstr



    # process article
    def updateCf(self, aCf: float) -> float:
        # formula to merge cf
        finalCf = self.__cf
        if(self.__cf >= 0 and aCf >= 0):
            finalCf = self.__cf + aCf * (1 - self.__cf)
        elif (self.__cf <= 0 and aCf <= 0):
            finalCf = self.__cf + aCf * (1 + self.__cf)
        elif ((self.__cf <= 0 <= aCf) or (self.__cf > 0 > aCf)):
            finalCf = (self.__cf + aCf) / (1 - min(abs(self.__cf), abs (aCf)))

        self.__cf = finalCf
        return finalCf


    def processArticle(self) -> bool:
        if not self.__articleProcessed:
            try:
                # newspleaseArticle = NewsPlease.from_url(self.__url)
                # self.__content = newspleaseArticle.maintext

                newspaperArticle = Article(self.__url)
                newspaperArticle.download()
                newspaperArticle.parse()
                newspaperArticle.nlp()
                successful = True
            except:
                self.__content = "Error fetching main containt of article Id: " + str(self.__id)
                successful = False

            if successful: # processing is successful
                self.__content = newspaperArticle.text
                self.__keywords = newspaperArticle.keywords
                self.__summary = newspaperArticle.summary
                if newspaperArticle.text == "":
                    self.__content = self.__description
                    self.__summary = self.__description
                if (len(self.__content) > 0):
                    self.__length = len(self.__content.split(' '))
                    self.__readingTime_min = float(self.__length) / self.__readingSpeed

            self.__articleProcessed = True

            return successful
