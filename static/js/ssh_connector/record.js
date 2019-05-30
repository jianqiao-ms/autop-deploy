function new_terminal() {
    let protocol    = (window.location.protocol.indexOf('https') === 0) ? 'wss' : 'ws';
    let ws_url      = protocol+'://'+window.location.host+ '/recordwebsocket';
    let ws          = new WebSocket(ws_url);
    let terminal    = new Terminal();
    let records     = {};
    
    
    ws.onopen = function (e) {
        ws.onmessage = function (e) {
            records.data = e.data;
        };
        ws.close();
        
    };

    
    window.onresize = function() { 
        terminal.fit();
    };
    
    terminal.open(document.getElementById('terminal-container'));
    return {records: records, terminal: terminal};
}

$(document).ready(function() {
    Terminal.applyAddon(fit);
    term = new_terminal();
    term.terminal.fit();
    term.terminal.write('456');
});