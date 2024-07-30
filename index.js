sessionToken = ""

function gettoken() {
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open( "POST", "/startsession", false );
	xmlHttp.setRequestHeader('Content-Type', 'application/json');
	xmlHttp.send( '{"username":"stratton","password":"hello"}' );
	sessionToken = xmlHttp.responseText
}

function makeaccount() {
	var xmlHttp = new XMLHttpRequest();
	xmlHttp.open( "POST", "/makeaccount", false );
	xmlHttp.setRequestHeader('Content-Type', 'application/json');
	xmlHttp.send( '{"username":"stratton","password":"hello","email":"stratjel@gmail.com"}' );
	if (xmlHttp.responseText != "ok") {
		alert("already taken ._.")
	}
}
