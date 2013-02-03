function restoreValues() {
	if (localStorage.serviceAddress) {
		document.getElementById('serviceAddress').value = localStorage.serviceAddress
	}
	if (localStorage.servicePort) {
		document.getElementById('servicePort').value = localStorage.servicePort
	}
}

function defaultValues() {
	document.getElementById('serviceAddress').value = "apple-tv.local"
	document.getElementById('servicePort').value = "8181"
}

function saveValues() {
	localStorage.serviceAddress = document.getElementById('serviceAddress').value
	localStorage.servicePort = document.getElementById('servicePort').value
	myAlert("Options saved!",
			"PlayIt extension will use saved values for further requests.")
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
document.addEventListener('DOMContentLoaded',restoreValues);
document.querySelector('#save').addEventListener('click',saveValues);
document.querySelector('#reset').addEventListener('click',defaultValues);
