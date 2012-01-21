var emailElems = document.getElementsByTagName("span");
for (var i = 0; i < emailElems.length; i++) {
	if (emailElems[i].className == "email")
		decodeEmailAddress(emailElems[i], false);
}


function decodeEmailAddress(elem, createLink) {  // Assumes child 0 is a text node
	var email = elem.firstChild.data;  // String
	email = email.replace(/ DOT /g, ".");
	email = email.replace(/ AT /g, "@");
	
	if (createLink) {
		var anchor = document.createElement("a");
		anchor.appendChild(document.createTextNode(email));
		anchor.href = "mailto:" + email;
		anchor.className = "external";
		elem.replaceChild(anchor, elem.firstChild);
	} else {
		elem.firstChild.data = email;
	}
}
