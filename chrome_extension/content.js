function makeRequest(tweet_id){
	// make request
    $.ajax({
        url: "https://192.168.56.1:8080",
        type: "POST",
		crossDomain: true,
        data: {tweet_id: tweet_id},
        dataType: "json",
        success: function(data) {
			window.alert("Success! PREDICTION = " + data.prediction);
			if (data.prediction !== "none") {
				var news_url = data.news_url;
				var img_url = chrome.extension.getURL("open.png");
				var new_div  = document.createElement('div');
				new_div.classList.add('hatespeech-extension-container');
				new_div.id = "hatespeech-extension-container-id";
				var html = "<div class='header-container bg-info text-white text-center text-big weight-300 pt-10px pb-10px'><img src='${img_url}'></div><div id='hatespeech-extension-content-container' class='hatespeech-extension-content-container pl-15px pr-15px pt-15px pb-15px' style='display:block'><div class='mb-15px'>Hi there. This tweet triggered our system, meaning it may contain a <a class='a' href='https://en.wikipedia.org/wiki/Hate_speech' target='_blank'>hateful</a> view. We know you like to keep an open mind and be well-read on the issues, so we did a Google search for a range of articles on this topic.</div><div class='weight-500 mb-15px'>Would you like to see what we found?</div><div class=''><a href='${news_url}' target='_blank' class='bttn bttn-lg bttn-block bttn-outline-success'>Yes, let's go!</a></div></div>";
				new_div.innerHTML = html.replace('${news_url}', news_url);
				new_div.innerHTML = html.replace('${img_url}', img_url);

				document.body.appendChild(new_div);
			}
        },
		error: function(xhr, ajaxOptions, thrownError) {
			window.alert("error!")
            // TODO: do nothing for now.
        }});
}
var url = window.location.href
var status_index = url.indexOf("status");
if (status_index > -1) {
	window.alert("Making request");
	makeRequest(url.substring(status_index + 7, url.legth));
}