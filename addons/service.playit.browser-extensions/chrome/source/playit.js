//PlayIt core function to send data to XBMC PlayIt port
function playIt(active_url) {
	serviceAddress = localStorage.serviceAddress
	servicePort = localStorage.servicePort
	if (!serviceAddress || !servicePort)
		myAlert('Options not set',
				'Using default values to connect. Check PlayIt extension options.')
	if (!serviceAddress) {
		serviceAddress = "apple-tv.local"
	}
	if (!servicePort) {
		servicePort = "8181"
	}

	service_url = "http://" + serviceAddress + ":" + servicePort + "/PlayIt"

	var playItService = new rpc.ServiceProxy(service_url, {
		asynchronous : true,
		protocol : "JSON-RPC",
		sanitize : false,
		methods : [ 'ping', 'playHostedVideo', 'playVideo' ]
	}, false);

	myAlert('Processing request',
			'Sending PlayIt request to XBMC, please wait...')

	try {
		playItService
				.playHostedVideo({
					params : {
						'videoLink' : active_url
					},
					onSuccess : function(responseObj) {
						title = responseObj.status
						if (responseObj.status === 'success')
							title = 'Playback started'
						else if (responseObj.status === 'error')
							title = 'Playback failed'
						else if (responseObj.status === 'exception')
							title = 'Unexpected error'
						myAlert(title, responseObj.message)
					},
					onException : function(err) {
						if (err != undefined && err.code != undefined
								&& err.code === 101)
							myAlert('Network error',
									'Unable to connect or request time-out. Check PlayIt extension setting.')
						else
							myAlert('Unknown error',
									'Chrome extension is unable to process request due to error.')
						return true
					},
					onComplete : function(responseObj) {
						// nothing
					}
				})

	} catch (err) {
		if (err != undefined && err.code != undefined && err.code === 101)
			myAlert('Network error',
					'Unable to connect or request time-out. Check PlayIt extension setting.')
		else
			myAlert('Unknown error',
					'Chrome extension is unable to process request due to error.')
	}

}

// Function to display HTML 5 notification to user.
function myAlert(title, msg) {
	title = 'PlayIt: ' + title
	if (webkitNotifications.checkPermission() == 0) {
		var notification = window.webkitNotifications.createNotification(
				'Icon-128.png', title, msg);
		notification.show();
		setTimeout(function() {
			notification.cancel()
		}, 2000);
	} else {
		alert(title + ' -> ' + msg)
	}
}

// Handles context menu item on click event
function cmClickHandler(info) {
	if (info.menuItemId == "playIt") {
		myAlert("Video selected", info.selectionText)
		playIt(info.linkUrl)
	}
}

// Handles add-on button click event
function buttonClickHandler() {
	chrome.tabs.getSelected(null, function(tab) {
		var active_url = tab.url;
		playIt(active_url);
	});
}

// Adds context menu item
chrome.runtime.onInstalled.addListener(function() {
	properties = {
		"type" : "normal",
		"title" : "PlayIt on XBMC",
		"id" : "playIt",
		"contexts" : [ "link" ],
		"onclick" : cmClickHandler
	};
	// Create a parent item and two children.
	chrome.contextMenus.create(properties);
});
chrome.browserAction.onClicked.addListener(buttonClickHandler);
