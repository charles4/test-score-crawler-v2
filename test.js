
console.log("Starting script");

var page = require('webpage').create();

/// this is a callback that enables console logs from the weppage to be printed in the terminal
page.onConsoleMessage = function (msg) {
    console.log(msg);
};

var login_url = 'https://www.assessmenttechnology.com/GalileoASP/ASPX/K12Login.aspx';

function doLogin(){
	page.evaluate(function() {
	        var username_input = document.querySelector("#txtUsername");
	        var password_input = document.querySelector("#txtPassword");
	        var loginForm = document.querySelector("#frmLogin");

	        username_input.value = "mcosta@scstucson.org";
	        password_input.value = "galileo";
	        loginForm.submit();
	});
};

//open the page
page.open(login_url);
page.onLoadFinished = function(status){
	console.log("Status:  " + status);
	console.log("Loaded:  " + page.url);
	console.log("state = " + (!phantom.state ? "no-state" : phantom.state));
	if (status === "success"){
		if (!phantom.state) {
			doLogin();
			phantom.state = "Step1"
		} else if ( phantom.state === "Step1") {
			page.render("after_login.png");
			phantom.exit();
		}
	} else {
		console.log("Unable to load webpage.");
	}
};

