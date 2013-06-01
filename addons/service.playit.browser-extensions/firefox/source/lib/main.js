// This is an active module of the ajdeveloped Add-on

var data = require("sdk/self").data
var prefs = require("sdk/simple-prefs").prefs
var cm = require("sdk/context-menu");
var widget = require("sdk/widget");
var tabs = require("tabs");
exports.main = function(){
    //Adding widget to addon menu    
    widget.Widget({
      id: "playit-btn",
      label: "PlayIt",
      contentURL: data.url("small-icon.png"), 
      onClick: function(){
        active_url = require("sdk/tabs").activeTab.url
        playIt(prefs.serviceAddress,prefs.servicePort,active_url)
      },
      onMouseover: function() {
        this.contentURL = data.url("Icon-32.png")
      },
      onMouseout: function() {
        this.contentURL = data.url("small-icon.png")
      }
    });
    
    widget.Widget({
     id: "playit-frameView-btn",
     label: "PlayIt Frame View",
     contentURL: data.url("view-icon.png"), 
     contentScriptWhen: "start",
     contentScriptUrl: data.url("view-inject.js"),
     onClick:function () {
      worker = tabs.activeTab.attach({
        contentScriptWhen: "start",
        contentScriptFile: [data.url("jquery-2.0.0.min.js"),data.url("view-inject.js")]
      });
      myAlert("PlayIt Frame View", "Please click on PlayIt bar appears on top of video frame.");
      worker.port.emit("viewFrame");
      worker.port.on("playItFrameAction", function (playItReq) {
        myAlert("Video selected", playItReq.url);
        playIt(prefs.serviceAddress,prefs.servicePort,playItReq.url);
      });
     },
      onMouseover: function() {
        this.contentURL = data.url("Icon-32.png")
      },
      onMouseout: function() {
        this.contentURL = data.url("view-icon.png")
      }
    });
    
    //Adding context menu item
    cm.Item({
      label: "PlayIt on XBMC",
      context: cm.SelectorContext("a[href]"),
      contentScript: 'self.on("click", function (node, data) {' +
                     '  self.postMessage([node.href,node.textContent.trim()]);' +
                     '});',
      onMessage: function (hyperlink) {
          myAlert("Video selected", hyperlink[1]);
          playIt(prefs.serviceAddress,prefs.servicePort,hyperlink[0]);
      }
    });

}


function playIt(serviceAddress, servicePort, active_url) {
    //service_url = "http://apple-tv.local:8181/PlayIt"
    service_url = "http://"+serviceAddress+":"+servicePort+"/PlayIt"
    console.log(service_url)
    rpc = require("rpc")
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
						console.log(err)
                        if (err != undefined && err.code != undefined
								&& err.code === 101)
							myAlert('Network error',
									'Unable to connect or request time-out. Check PlayIt add-on preferences.')
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
					'Unable to connect or request time-out. Check PlayIt add-on preferences.')
		else
			myAlert('Unknown error',
					'Firefox extension is unable to process request due to error.')
	}

}
function myAlert(title, msg) {
	title = 'PlayIt: ' + title
    var myIconURL = data.url("Icon-96.png");
	require("sdk/notifications").notify({
        title: title,
        text: msg,
        iconURL: myIconURL
    });
}

/*
var ss = require("sdk/simple-storage");
var playItPanel = require("sdk/panel").Panel({
  width:350,
  height:175,
  contentURL: data.url("playIt-panel.html"),
  contentScriptFile: data.url("playIt-panel.js"),
  contentScriptWhen:"ready"
});


widget.port.on("playIt", function(){
  myAlert("LEFT Click","play the current active url");
  playIt(ss.storage.serviceAddress, ss.storage.servicePort)
});
 
widget.port.on("open-settings", function(){
  myAlert("RIGHT Click","open settings panel");
  playItPanel.show();
});


playItPanel.port.on("save", function(params){
  myAlert("Save values input by user, value:", params);
  ss.storage.serviceAddress = params.serviceAddress;
  ss.storage.servicePort = params.servicePort;
  myAlert("Save successful!","The user input values hvae been saved.")
  playItPanel.hide()
});

*/
