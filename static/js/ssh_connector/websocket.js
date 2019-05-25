function wsconnect(terminal) {
    terminal.reset();
    var ws = new WebSocket("ws://192.168.2.200:60000/websocket");
    ws.onmessage = function (e) {
        console.log(e);
        terminal.write(e.data);
    };
    return ws
}
$(document).ready(function() {
    Terminal.applyAddon(fit);
    Terminal.applyAddon(fullscreen);
    
    let terminal = new Terminal();
    terminal.open(document.getElementById('terminal-container'));
    
    let ws = wsconnect(terminal);
    
    terminal.on('data', function (data) {
        console.log(ws.readyState);
        if (ws.readyState === 3 || ws.readyState === 2) {
            ws = wsconnect(terminal);
        } else {
            ws.send(data);
        }
    });
    terminal.toggleFullScreen(); 
    terminal.fit();

});