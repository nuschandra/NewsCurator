from typing import List
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
import string
import requests

class Keyphrase():
    def __init__(self, aKeywords: List[str], aStrength: float):
        self.__keywords = aKeywords
        self.__strength = aStrength

    @property
    def strength(self) -> float: return self.__strength

    @strength.setter
    def strength(self, aValue: float): self.__strength = aValue

    @property
    def keywords(self) -> [str]: return self.__keywords

    @keywords.setter
    def keywords(self, aValue: [str]): self.__keywords = aValue



class KeywordMatcher():
    def __init__(self, aCountryName: str = ""):
        self.__keyphrases = self.getCountryKeyphrases(aCountryName) if len(aCountryName) > 0 else []

    @property
    def keyphrases(self) -> [Keyphrase]: return self.__keyphrases

    @keyphrases.setter
    def keyphrases(self, aValue: [Keyphrase]): self.__keyphrases = aValue


    def prepText(self, text: str):
        # split into words
        tokens = word_tokenize(text)

        # remove punctuation from each word
        table = str.maketrans('', '', string.punctuation)
        stripped = [w.translate(table) for w in tokens]

        # remove remaining tokens that are not alphabetic
        words = [word for word in stripped if word.isalpha()]

        # filter out stop words
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]

        stemer = LancasterStemmer()
        #words = [stemer.stem(w) for w in words]

        # convert to lower case
        words = [w.lower() for w in words]

        return words

    def getCountryKeyphrases(self, aCountry: str) -> [Keyphrase]: # get words related to country from ConceptNet
        country = aCountry.replace(" ", "_").lower()
        results = requests.get('http://api.conceptnet.io//related/c/en/' + country + '?filter=/c/en').json()

        relatedWords = []
        stemer = LancasterStemmer()
        for r in results['related']:
            temp = r['@id'].split('/')
            keywords = temp[len(temp) - 1].split('_')
            #keywords = [stemer.stem(w) for w in keywords]
            wt = r['weight']
            relatedWords.append(Keyphrase(keywords, wt))

        if "america" in country:
            relatedWords.append(Keyphrase(["american"], 0.99))
            relatedWords.append(Keyphrase(["americans"], 0.99))
            relatedWords.append(Keyphrase(["us"], 0.99))
        elif country == "singapore":
            relatedWords.append(Keyphrase(["singaporeans"], 0.99))
            relatedWords.append(Keyphrase(["spore"], 0.99))

        return relatedWords

    def computeMatchingScore(self, aArticle: str, aKeyphrases: [Keyphrase] = None) -> float:
        articleWords = self.prepText(aArticle)
        countryKeyphrases = self.__keyphrases if aKeyphrases == None else aKeyphrases
        score = 0.0

        for i in range(len(articleWords)):
            for cntryWord in countryKeyphrases:
                match = False
                for j in range(len(cntryWord.keywords)):
                    if(i + j < len(articleWords)):
                        match = articleWords[i+j] == cntryWord.keywords[j]
                        if not match: break
                    else:
                        match = False
                        break
                # next j
                if match: # a word or phrase in the article matches with the country key word or phrase
                    score += cntryWord.strength
            # next cntryWord
        # next i
        score = score / (len(articleWords) + 1)

        return score

    def trendingNewsScore(self, trending_headline_keywords, articleKeywords):
        stemer = LancasterStemmer()
        count = 0
        if (len(trending_headline_keywords) != 0 and len(articleKeywords) != 0):
            trending_headline_keywords_stemmed = [stemer.stem(w) for w in trending_headline_keywords]
            articleKeywords_stemmed = [stemer.stem(w) for w in articleKeywords]
            for i in trending_headline_keywords_stemmed:
                for j in articleKeywords_stemmed:
                    if i == j:
                        count+=1
                        if count >= 2: return True
                
        return False