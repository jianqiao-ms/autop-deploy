function new_terminal() {
    let protocol    = (window.location.protocol.indexOf('https') === 0) ? 'wss' : 'ws';
    let ws_url      = protocol+'://'+window.location.host+ '/websocket';
    let ws          = new WebSocket(ws_url);
    let terminal    = new Terminal();

    
    ws.onopen = function (event) {
        ws.onmessage = function (event) {
            json_msg = JSON.parse(event.data);
            switch(json_msg['type']) {
                case 'stdout':
                    terminal.write(json_msg['data']);
                    break;
                case 'disconnect':
                    ws.close();
                    break;
            }
        };
        terminal.on('data', function (e) {
            console.log(e);
            ws.send(JSON.stringify({
                'type' : 'stdin',
                'data' : e
            }));
        });
        terminal.on('resize', function () {
            console.log('resize');
            ws.send(JSON.stringify({
                'type' : 'resize',
                'data' : [
                    terminal.cols,
                    terminal.rows
                ]
            }));
        });

    };
    
    terminal.open(document.getElementById('terminal-container'));
    return {socket: ws, terminal: terminal};
    
    

}

$(document).ready(function() {
    Terminal.applyAddon(fit);
    Terminal.applyAddon(fullscreen);
    
    let term = new_terminal();
    term.terminal.toggleFullScreen(); 
    term.terminal.fit();
    
    window.onresize = function() { 
        term.terminal.toggleFullScreen(true); 
        term.terminal.fit();
    };
});