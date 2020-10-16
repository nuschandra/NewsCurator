from app import app
from flask import request, Markup, render_template, jsonify, session, make_response
from app.business import cf_data
from app.model.user_preferences import UserPreferences, UserPreferencesSchema
from app.model.user_preferences import UserPreferences, UserPreferencesSchema
from app.model.topics import Topics
from app.model.news_topics import NewsTopics
from app.model.interest_levels import InterestLevels
from app.model.countries import Countries
from app import db
from app.business.process_news_articles import ProcessNewsArticles

users = []

def retrieveTopicsAndPreferencesToShow():
    news_topics = [i.value for i in NewsTopics]
    general_preferences = [i.generalPreferences for i in InterestLevels]
    topic_preferences = [i.topicPreferences for i in InterestLevels]
    source_preferences = [i.sourcePreferences for i in InterestLevels]

    # retrieve record from database using userid
    user_id = int(request.cookies["newscurator_userid"]) if "newscurator_userid" in request.cookies else -1
    userprofile = UserPreferences.query.filter_by(id=user_id).first()
    userprofileJson = "null" if userprofile == None else userprofile.getJsonStr()

    return news_topics, general_preferences, topic_preferences, source_preferences, userprofileJson

@app.route('/userPreferences', methods = ['POST'])
def createUserPreferences():
    user_id = UserPreferencesSchema().load(request.get_json())
    print(user_id)
    #showNewsArticles()
    return jsonify(userId = user_id), 200

@app.route("/userProfile", methods=["GET"])
def showUserProfile():
    user_email = request.cookies.get('newscurator_useremail')
    news_topics, general_preferences, topic_preferences, source_preferences, userprofileJson = retrieveTopicsAndPreferencesToShow()

    return render_template("user_profile.html", newsTopics=Markup(news_topics),
                           topicPref=Markup(topic_preferences), generalPref=Markup(general_preferences),
                           srcPref=Markup(source_preferences), countries=Markup(Countries.getCountries()),
                           userprofile=Markup(userprofileJson), userEmail=user_email) #app.newsapp_active_user)

@app.route("/newsarticles", methods = ["GET"])
def showNewsArticles():
    user_id = request.args.get('id')
    user_email = request.cookies.get('newscurator_useremail')
    article_type = request.args.get('articletype')
    user_profile = UserPreferences.query.filter_by(id=user_id).first()
    print(user_profile.user_name)
    if user_profile != None:
        newsArticles = ProcessNewsArticles().fetchNewsArticles(user_profile, article_type)
        articlesJson = ProcessNewsArticles().rankNewsArticles(user_profile, newsArticles, article_type)
    else:
        articlesJson = "null"
    return render_template("newsarticles.html", articles=Markup(articlesJson), userEmail=user_email) #app.newsapp_active_user)

@app.route("/")
@app.route("/login", methods=["POST", "GET"])
def showLogin():
    news_topics, general_preferences, topic_preferences, source_preferences, userprofileJson = retrieveTopicsAndPreferencesToShow()

    user_email = request.cookies.get("newscurator_useremail") if "newscurator_useremail" in request.cookies else ""
    if request.method == "POST":
        if request.form["submitBtn"] == "signIn":
            user_email = request.form["email"]
            # session["USEREMAIL"] = request.form["email"]
            # app.newsapp_active_user = session["USEREMAIL"]
            resp = make_response(render_template("user_profile.html", newsTopics=Markup(news_topics),
                                                 topicPref=Markup(topic_preferences), generalPref=Markup(general_preferences),
                                                 srcPref=Markup(source_preferences), countries=Markup(Countries.getCountries()),
                                                 userprofile=Markup(userprofileJson), userEmail=user_email))
            resp.set_cookie("newscurator_useremail", user_email)
            return resp
        elif request.form["submitBtn"] == "signOut":
            user_email = ""
            # session.pop("USEREMAIL", None)
            # app.newsapp_active_user = ""

    resp = make_response(render_template("login.html", userEmail=user_email))
    resp.set_cookie("newscurator_useremail", user_email)
    return resp
    # return render_template("login.html", userEmail=user_email) #app.newsapp_active_user)