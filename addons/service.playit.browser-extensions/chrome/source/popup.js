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

clicker = document.querySelector('#playIt').addEventListener('click',
		playActiveURL, false);
dialog = document.querySelector('#frameView').addEventListener('click',
		playItFrameView, false);
