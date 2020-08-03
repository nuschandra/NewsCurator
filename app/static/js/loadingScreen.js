function showLoading(senderId, idToHide)
{
    if(senderId == "saveProfileBtn")
    {
        if($("#formCheck-1"). prop("checked") == true)
        {
            $("#loadingScreen").css("display", "block");
            $("#" + idToHide).css("display", "none");
        }
    }
    else
    {
        $("#loadingScreen").css("display", "block");
        $("#" + idToHide).css("display", "none");
    }
    return true;
}

function toggleLoginIcon()
{
    if ($("#userEmail").text().length > 0) // user is logged in
    {
        var loginBtn = $("#loginBtn");
        loginBtn.text().replace("Sign In", "A");

        $("#loginIcon").css("display", "block");

        $(".form-group.signInBtn").css("display", "none");
        $(".form-group.signOutBtn").css("display", "block");
    }
    else
    {
        var loginBtn = $("#loginBtn");
        var newText = "Sign In" + loginBtn.text();
        loginBtn.text(newText);

        $("#loginIcon").css("display", "none");

        $(".form-group.signInBtn").css("display", "block");
        $(".form-group.signOutBtn").css("display", "none");
    }
}

function toggleLoginButton()
{
    if ($("#userEmail").text().length > 0) // user is logged in
    {
        $(".form-group.signInBtn").css("display", "none");
        $(".form-group.signOutBtn").css("display", "block");
    }
    else
    {
        $(".form-group.signInBtn").css("display", "block");
        $(".form-group.signOutBtn").css("display", "none");
    }
}

