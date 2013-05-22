function playActiveURL() {
	window.close();
	var playIt = chrome.extension.getBackgroundPage();
	playIt.playItRequestHandler();
}
function playItFrameView() {
	window.close();
	var playIt = chrome.extension.getBackgroundPage();
	playIt.playItFrameViewEnabler();
}

function trackButtonClick(e) {
	_gaq.push([ '_trackEvent', e.target.id, 'clicked' ]);
};

document.querySelector('#playIt').addEventListener('click', playActiveURL);
document.querySelector('#frameView').addEventListener('click', playItFrameView);

var buttons = document.querySelectorAll('button');
for ( var i = 0; i < buttons.length; i++) {
	buttons[i].addEventListener('click', trackButtonClick);
}

var _gaq = _gaq || [];
_gaq.push([ '_setAccount', 'UA-22779680-5' ]);
_gaq.push([ '_trackPageview' ]);

(function() {
	var ga = document.createElement('script');
	ga.type = 'text/javascript';
	ga.async = true;
	ga.src = 'https://ssl.google-analytics.com/ga.js';
	var s = document.getElementsByTagName('script')[0];
	s.parentNode.insertBefore(ga, s);
})();