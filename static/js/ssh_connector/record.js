import '../../xterm/xterm.js';
import '../../xterm/addons/fullscreen/fullscreen.js';
Terminal.applyAddon(fullscreen);

import {Timeline} from "./timeline.js";



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
        timeline.stop();
    };
    window.onresize = function() { 
        terminal.toggleFullScreen(true);
    };

    terminal.open(document.getElementById('terminal-container'));
    terminal.toggleFullScreen(true);
    
    return timeline
}

$(document).ready(function() {
    let timeline = new_terminal();
    
    // setTimeout(function () {
    //     timeline.pause()
    // }, 1500)
    
    
});