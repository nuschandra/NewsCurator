//$(document).ready(function(){
//    // new Sources
//    var sources = null;
//    addNewSources(sources);
//});

function addNewSources(aNewsSources){
    // news Sources
    var sources = ["CNA", "The Straits Times", 
                    "AsiaOne", "TODAYonline",
                    "Theindependent.sg", "Google News",
                    "Financial Times", "Business Times",
                    "Space Daily", "Phys.Org",
                    "TechRadar", "Digitalmarketnews.com",
                    "Ubergizmo", 
                    "Mashable", "Yahoo Entertainment",
                    "soompi", "The Verge",
                    "Sporting News", "ESPN" ];
    
    if(aNewsSources == null) { aNewsSources = sources; }
	var tableRef = $('#newsSourceTable')[0];
    
	for(var i = 0; i < aNewsSources.length; i+=3)
	{
        //console.log(i);
		var newRow = tableRef.insertRow();
        
        var newCell  = newRow.insertCell(-1);
        newCell.innerHTML = aNewsSources[i] + '<select class="form-control source" name="src_' + aNewsSources[i] + '"></select>';
			
        if(aNewsSources.length - 1 > i + 1)
        {
            newCell  = newRow.insertCell(-1);
            newCell.innerHTML = aNewsSources[i+1] + '<select class="form-control source" name="src_' + aNewsSources[i+1] + '"></select>';
        }
        
        if(aNewsSources.length - 1 > i + 2)
        {
            newCell  = newRow.insertCell(-1);
            newCell.innerHTML = aNewsSources[i+2] + '<select class="form-control source" name="src_' + aNewsSources[i+2] + '"></select>';
        }
	}
}