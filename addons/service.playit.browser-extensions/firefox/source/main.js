// This is an active module of the ajdeveloped Add-on

var data = require("self").data
exports.main = function(){
    require("widget").Widget({
      id: "playit-btn",
      label: "PlayIt",
      contentURL: data.url("small-icon.png"),
      panel: playItPanel,
      onMouseover: function() {
        this.contentURL = data.url("Icon-32.png")
      },
      onMouseout: function() {
        this.contentURL = data.url("small-icon.png")
      }
    });
}

var playItPanel = require("panel").Panel({
  width:400,
  height:150,
  contentURL: data.url("playIt-panel.html"),
  contentScriptFile: data.url("playIt-panel.js"),
  contentScriptWhen:"ready"
});


playItPanel.port.on("playItEvent", function(params) {
    //service_url = "http://apple-tv.local:8181/PlayIt"
    service_url = "http://"+params.serviceAddress+":"+params.servicePort+"/PlayIt"
    console.log(service_url)
    rpc = require("rpc")
    var playItService = new rpc.ServiceProxy(service_url, {
    			asynchronous : true,
				protocol : "JSON-RPC",
				sanitize : false,
				methods : [ 'ping', 'playHostedVideo', 'playVideo' ]
			}, false);
    
	active_url = require("tabs").activeTab.url
	myAlert('Processing request',
			'Sending PlayIt request to XBMC, please wait...')
    playItPanel.hide()
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
						console.log(err)
                        if (err != undefined && err.code != undefined
								&& err.code === 101)
							myAlert('Network error',
									'Unable to connect or request time-out. Check PlayIt extension setting.')
						else
							myAlert('Unknown error',
									'Firefox extension is unable to process request due to error.')
						return true
					},
					onComplete : function(responseObj) {
						//nothing
					}
				})

	} catch (err) {
		console.log(err)
        if (err != undefined && err.code != undefined
				&& err.code === 101)
			myAlert('Network error',
					'Unable to connect or request time-out. Check PlayIt extension setting.')
		else
			myAlert('Unknown error',
					'Firefox extension is unable to process request due to error.')
	}

});
function myAlert(title, msg) {
	title = 'PlayIt: ' + title
    var myIconURL = data.url("Icon-96.png");
	require("notifications").notify({
        title: title,
        text: msg,
        iconURL: myIconURL
    });
}