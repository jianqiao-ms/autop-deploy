import '../../xterm/xterm.js';
import '../../xterm/addons/fit/fit.js';
import '../../xterm/addons/fullscreen/fullscreen.js';
Terminal.applyAddon(fit);
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
    let timeline = new_terminal();
    let btnPlay = $('#terminal-play-control > div.d-flex.flex-row.text-secondary.fa-3x.mt-2 > svg.svg-inline--fa.fa-play-circle.fa-w-16');
    let btnStop = $('#terminal-play-control > div.d-flex.flex-row.text-secondary.fa-3x.mt-2 > svg.svg-inline--fa.fa-stop-circle.fa-w-16');
    
    btnPlay.click(function () {
        console.log('Start button clicked');
        timeline.start_play();
    });
    
    
    // setTimeout(function () {
    //     timeline.pause()
    // }, 1500)
    
    
});