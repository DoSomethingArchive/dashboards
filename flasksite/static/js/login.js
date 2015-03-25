//get logged in basic google profile data
var profile_info = {};

function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  profile_info.name = profile.getName();
  profile_info.email = profile.getEmail();
  var t = document.getElementById("g_text_form");
  t.value = profile_info.email;
}

//once profile data exists, submits form
function loginFormSubmit() {
  var checkExist = setInterval(
    function () {
      //checks if email element exists yet
      if (profile_info.email ? true : false == true ) {
        document.getElementById("login_form").submit();
        clearInterval(checkExist);
      }
    }, 1000
  );
}