function showLoading(idToHide)
{
    $("#loader").css("display", "block");
    $("#" + idToHide).css("display", "none");
    return true;
}