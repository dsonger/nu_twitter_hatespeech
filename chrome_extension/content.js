// this is currently for demo purposes
var url = "" + window.top.location;
var trimmed_string = url.substring(20);
var query_string = trimmed_string.substring(0,trimmed_string.indexOf("/"));
//

if (url.indexOf("status") > -1) {	
	
	var new_div  = document.createElement('div');

	new_div.classList.add('hatespeech-extension-container');
	new_div.id = "hatespeech-extension-container-id";
	var html = "<div class='header-container bg-info text-white text-center text-big weight-300 pt-10px pb-10px'><div class=''>OPEN Detector</div></div><div id='hatespeech-extension-content-container' class='hatespeech-extension-content-container pl-15px pr-15px pt-15px pb-15px' style='display:block'><div class='mb-15px'>Hi there. This tweet triggered our system, meaning it may contain a <a class='a' href='https://en.wikipedia.org/wiki/Hate_speech' target='_blank'>hateful</a> view. We know you like to keep an open mind and be well-read on the issues, so we did a Google search for a range of articles on this topic.</div><div class='weight-500 mb-15px'>Would you like to see what we found?</div><div class=''><a href='https://google.com/search?q=${query_string}' target='_blank' class='bttn bttn-lg bttn-block bttn-outline-success'>Yes, let's go!</a></div></div>";
	new_div.innerHTML = html.replace('${query_string}', query_string);

	document.body.appendChild(new_div);
}



// var img_url = chrome.extension.getURL("logo.jpg");
// document.getElementById("logo-img").src = img_url;