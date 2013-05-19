var handlePlayItAction = function(event) {
	console.log("Got playit action for URL = " + event.data);
	safari.self.tab.dispatchMessage("playIt", event.data);
}

var seekForFrameAndEmbed = function() {
	$("iframe,embed")
			.each(
					function() {
						var src = $(this).attr("src");
						var height = $(this).height();
						var width = $(this).width();

						if (src !== undefined && src.match("^http")
								&& height > 300 && width > 300) {

							var div = $("<div style=\"position:absolute; background-color:black; opacity:0.4; font-variant: small-caps; font-family:tahoma; font-weight:bold; font-size:16px; color:white;\"></div>");
							div.hover(function() {
								div.css('opacity', '0.7');
								div.css('cursor', 'hand');
								div.css('cursor', 'pointer');
							}, function() {
								div.css('opacity', '0.4');
							});

							var img = $("<img style=\"background-color:white; opacity:0.6; position: absolute;\"/>");
							img.attr("src", safari.extension.baseURI
									+ "Icon-64.png");

							var top = $(this).scrollTop();
							var left = $(this).scrollLeft();

							img.scrollTop(top + 5);
							if (left !== 0) {
								img.scrollLeft(left + 5);
							}
							div.click(src, handlePlayItAction)

							div.width(width);
							div.height(65);
							div.scrollTop(top);
							if (left !== 0) {
								div.scrollLeft(left);
							}
							$(this).before(div);
							div.append(img);
							div
									.append('<p style=" text-align: center; margin-left: 80px;">PlayIt on XBMC</p>');
						}
					});

}

function respondToMessage(theMessageEvent) {
	if (theMessageEvent.name === "showFrameView") {
		seekForFrameAndEmbed();
	}
}

safari.self.addEventListener("message", respondToMessage, false);
