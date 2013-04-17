//Context menu listener
document.addEventListener("contextmenu", handleContextMenu, false);
//This function adds information about the hyperlink on which context menu opened.
function handleContextMenu(event) {
	if(event.target.nodeName == 'A'){
		safari.self.tab.setContextMenuEventUserInfo(event, [event.target.href,event.target.textContent.trim()]);
	}
}
