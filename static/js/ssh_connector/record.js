import '../../xterm/xterm.js';
import '../../xterm/addons/fit/fit.js';
import {Timeline} from "./timeline.js";

Terminal.applyAddon(fit);


function new_terminal() {
    let protocol    = (window.location.protocol.indexOf('https') === 0) ? 'wss' : 'ws';
    let ws_url      = protocol+'://'+window.location.host+ '/recordwebsocket';
    let ws          = new WebSocket(ws_url);
    let terminal    = new Terminal();
    let timeline    = new Timeline(terminal);

    ws.onopen = function (e) {
        ws.onmessage = function (ee) {
            timeline.open(ws, ee);
        };
    };
    ws.onclose = function (ee) {
        timeline.start_play();
    };
    window.onresize = function() { 
        terminal.fit();
    };

    terminal.open(document.getElementById('terminal-container'));
    terminal.fit();
    
    return timeline
}

$(document).ready(function() {
    let timeline = new_terminal();
    
    setTimeout(function () {
        timeline.pause()
    }, 1500)
    
    
});