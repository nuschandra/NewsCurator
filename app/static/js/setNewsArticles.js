function setNewsArticles(aArticlesList)
{
//    {
//    "id": 0,
//    "title": "news title",
//    "url": "error url",
//    "description": "news Desc",
//    "source": "News Source",
//    "topic": "Health",
//    "date": 3,
//    "isTreading": true,
//    "isLocalNews": true,
//    "readingSpeed": 250.0,
//    "articleProcessed": true,
//    "content": "Sample Content",
//    "length": 2,
//    "readingTime_min": 0.008,
//    "keywords": ["a", "b"],
//    "summary": "",
//    "cf": 0.6456000000000001
//    }

    if(aArticlesList != null)
    {
        for(var i = 1; i <= 5; i++)
        {
            if (i <= aArticlesList.length)
            {
                var article = JSON.parse(aArticlesList[i-1]);

                $("#article-title-" + i).html(article.title + " (cf: " + article.cf.toFixed(4) + ")"); // set title

                // set link
                var articleLink = $("#article-link-" + i);
                articleLink.attr("href", article.url);
                articleLink.html(article.url);

                // set topic
                var d = new Date();
                d.setDate(d.getDate() - article.date);
                var trending = '';
                if (article.isTreading) { trending = ' | Trend'; }
                var local = '';
                if (article.isLocalNews) {local = ' | Local'; }
                $("#article-topic-" + i).val('[' + article.topic + local + trending + "] (Published: " + formatDate(d)  + ")");
                //console.log(article)

                $("#article-keyword-" + i).html("keywords: " + article.keywords.join(", ")); // set keywords
                $("#article-summary-" + i).html(article.summary); // set summary
            }
        }

        for(var i = 6; i <= 10; i++)
        {
            if (i <= aArticlesList.length)
            {
                var article = JSON.parse(aArticlesList[i-1]);
                var link = $("#article-link-" + i);
                link.attr("href", article.url); // set link
                var trending = '';
                if (article.isTreading) { trending = ' | Trend'; }
                var local = '';
                if (article.isLocalNews) {local = ' | Local'; }
                link.html("[" + article.topic + local + trending + "] " + article.title + " (cf: " + article.cf.toFixed(4) +")"); // set title
            }
        }
    }
}

function formatDate(date)
{
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    return [year, month, day].join('/');
}