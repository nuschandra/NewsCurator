function setNewsArticles(aArticlesList)
{
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
                articleLink.html(article.url.substring(0,47) + '...');

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

function getCookie(cname)
{
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++)
  {
    var c = ca[i];
    while (c.charAt(0) == ' ')
    {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) { return c.substring(name.length, c.length); }
  }
  return "";
}

function fetchWorkArticles()
{
    //var userId = document.cookie;
    //var elements = userId.split('=');
    //var id = elements[1]
    var id = getCookie("newscurator_userid")
    console.log(id)
    localStorage.setItem('article_type', 'Profession');
    url = window.location.protocol + "//" + window.location.host + "/newsarticles?id="+ id + '&articletype=Profession';
    console.log(url);
    window.location.href = url;
}

function fetchLeisureArticles()
{
    //var userId = document.cookie;
    //var elements = userId.split('=');
    //var id = elements[1]
    var id = getCookie("newscurator_userid")
    console.log(id)
    localStorage.setItem('article_type', 'Leisure');
    url = window.location.protocol + "//" + window.location.host + "/newsarticles?id="+ id + '&articletype=Leisure';
    console.log(url);
    window.location.href = url;
}

function activateWorkLeisureLink()
{
    if (localStorage.getItem('article_type').toUpperCase() == "PROFESSION") {
        $("#workarticles-link").attr('class', 'nav-link active');
        $("#leisurearticles-link").attr('class', 'nav-link');
    }
    else{
        $("#workarticles-link").attr('class', 'nav-link');
        $("#leisurearticles-link").attr('class', 'nav-link active');
    }
}