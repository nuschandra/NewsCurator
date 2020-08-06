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

function setCountries(aCountries)
{
    var select = $(".form-control.country")[0];
    $(select).find('optgroup, option').remove();

    for(var code in aCountries)
    {
        var countryName = aCountries[code];
        var selected = "";
        if(code == "sg") { selected = "selected"; }
        $(select).append('<option value="' + code + '" ' +  selected + '>' + countryName + '</option>');
    }
}