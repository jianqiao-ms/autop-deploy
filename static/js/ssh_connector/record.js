import '../../xterm/xterm.js';
import '../../xterm/addons/fit/fit.js';
import '../../xterm/addons/fullscreen/fullscreen.js';

Terminal.applyAddon(fit);
Terminal.applyAddon(fullscreen);

import {Timeline} from "./timeline.js";



function new_timeline() {
    let protocol    = (window.location.protocol.indexOf('https') === 0) ? 'wss' : 'ws';
    let ws_url      = protocol+'://'+window.location.host+ '/recordwebsocket';
    let ws          = new WebSocket(ws_url);
    let terminal    = new Terminal();
    let timeline    = new Timeline(terminal);

    ws.onopen = function (e) {
        ws.onmessage = function (ee) {
            terminal.open(document.getElementById('terminal-container'));
            terminal.fit();
            terminal.toggleFullScreen(true);
            timeline.open(ws, ee);
        };
    };
    ws.onclose = function (ee) {
        timeline.stop();
    };
    window.onresize = function() { 
        terminal.fit();
        terminal.toggleFullScreen(true);
    };

    
    
    return timeline
}

$(document).ready(function() {
    new_timeline();
    
    // setTimeout(function () {
    //     timeline.pause()
    // }, 1500)
    
    
});