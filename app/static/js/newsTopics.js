//$(document).ready(function(){
//    // new Sources
//    var sources = null;
//    addNewSources(sources);
//});

function addNewsTopics(aNewsTopics){
    // news topics
	var tableRef = {}
	tableRef["work_"] = $('#workTopicsTable')[0];
	tableRef["leis_"] = $('#leisureTopicsTable')[0];

    for(var key in tableRef)
    {
        for(var i = 0; i < aNewsTopics.length; i+=3)
        {
            var newRow = tableRef[key].insertRow();

            var newCell  = newRow.insertCell(-1);
            newCell.innerHTML = aNewsTopics[i] + '<select class="form-control topics" name="' + key + aNewsTopics[i] + '"></select>';

            if(aNewsTopics.length - 1 > i + 1)
            {
                newCell  = newRow.insertCell(-1);
                newCell.innerHTML = aNewsTopics[i+1] + '<select class="form-control topics" name="' + key + aNewsTopics[i+1] + '"></select>';
            }

            if(aNewsTopics.length - 1 > i + 2)
            {
                newCell  = newRow.insertCell(-1);
                newCell.innerHTML = aNewsTopics[i+2] + '<select class="form-control topics" name="' + key + aNewsTopics[i+2] + '"></select>';
            }
        }
    }

}