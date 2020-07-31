//$(document).ready(function(){
//    // Topic preferences
//    var pref = ["not related", "unlikely to be related", "not sure", "likely to be related", "related"];
//    setPreferences(pref, ".form-control.topics");
//
//    // general preferences
//    pref = ["Definitely!", "I suppose ", "No preference"];
//    setPreferences(pref, ".form-control.general");
//
//    // new source preferences
//    pref = ["I don’t want to see this source ",
//            "I prefer not seeing this source ",
//            "No preference ",
//            "I prefer seeing this source ",
//            "I only want to see this source "];
//    setPreferences(pref, ".form-control.source");
//});

function setPreferences(aPref, aClassName){
    var select = $(aClassName);
    //console.log(aPref.length);
    
    for (var j = 0; j < select.length; j++)
    {
        $(select[j]).find('optgroup, option').remove();

        for(var i = 0; i < aPref.length; i++)
        {
            var selected = "";
            if(i == 2) { selected = "selected"; }
            $(select[j]).append('<option value="' + aPref[i] + '" ' +  selected + '>' + aPref[i]+ '</option>');
        }
        //$(select[j]).append('<option value="' + aPref.length + '" >' + 'hello' + '</option>');
    }
}