function restoreValues(event) {
	if (localStorage.serviceAddress) {
		document.getElementById('serviceAddress').value = localStorage.serviceAddress
	}
	if (localStorage.servicePort) {
		document.getElementById('servicePort').value = localStorage.servicePort
	}
}

function defaultValues(event) {
	document.getElementById('serviceAddress').value = "apple-tv.local"
	document.getElementById('servicePort').value = "8181"
}

function saveValues(event) {
	var serviceAddress = document.getElementById('serviceAddress').value;
	var servicePort = document.getElementById('servicePort').value;
	localStorage.serviceAddress = serviceAddress
	localStorage.servicePort = servicePort
	myAlert("Options saved!",
			"PlayIt extension will use saved values for further requests.")
//
//	var serviceUrl = 'http://' + serviceAddress + ':' + servicePort + '/PlayIt';
//	chrome.permissions
//			.contains(
//					{
//						origins : [ serviceUrl ]
//					},
//					function(result) {
//						if (result) {
//							localStorage.serviceAddress = serviceAddress
//							localStorage.servicePort = servicePort
//
//							myAlert("Options saved!",
//									"PlayIt extension will use saved values for further requests.")
//						} else {
//
//						}
//					});
//	chrome.permissions
//			.request(
//					{
//						origins : [ serviceUrl ]
//					},
//					function(granted) {
//						alert(granted)
//						if (granted) {
//							localStorage.serviceAddress = serviceAddress
//							localStorage.servicePort = servicePort
//
//							myAlert("Options saved!",
//									"PlayIt extension will use saved values for further requests.")
//						} else {
//							myAlert("Permission Grant Denied",
//									"PlayIt extension has NOT saved the entered values.")
//						}
//					});
	return false;
}

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
document.addEventListener('DOMContentLoaded', restoreValues);
document.querySelector('#save').addEventListener('click', saveValues);
document.querySelector('#reset').addEventListener('click', defaultValues);
