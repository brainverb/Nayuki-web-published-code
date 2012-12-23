var activelink = null;

var container = document.getElementById("videolinks");
var links = container.getElementsByTagName("a");
for (var i = 0; i < links.length; i++) {
	var anchor = links[i];
	var match = /^http:\/\/www\.youtube\.com\/watch\?v=([A-Za-z0-9_-]{11})$/.exec(anchor.href);
	if (match != null) {
		function makeOnclickHandler(elem, url) {
			return function() {
				document.getElementById("videoframe").src = url;
				if (activelink != null)
					activelink.className = "";
				elem.className = "activelink";
				activelink = elem;
				return false;
			};
		}
		var func = makeOnclickHandler(anchor, "http://www.youtube.com/embed/" + match[1]);
		anchor.onclick = func;
		if (i == 0)
			func();
	}
}
