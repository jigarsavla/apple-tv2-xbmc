document.getElementById("playit").onclick=function(){
    data = {
        'serviceAddress':document.getElementById('serviceAddress').value,
        'servicePort':document.getElementById('servicePort').value
    }
    console.log(data.serviceAddress)
    self.port.emit("playItEvent", data);
}