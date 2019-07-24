//
container = $("div.terminal-container");


// Terminal.applyAddon(fit);
var term = new Terminal({
    "cursorBlink":true
});
term.open(document.getElementById('terminal'));
var ws = new WebSocket("ws://"+ window.location.host +"/websocket");

ws.onmessage = function (e) {
    console.log(e);
    term.write(e.data);
};

term.on('data', function (data) {
    console.log(data);
    ws.send(data);
});