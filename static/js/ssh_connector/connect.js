import '../../xterm/xterm.js';
import '../../xterm/addons/fit/fit.js';
import '../../xterm/addons/fullscreen/fullscreen.js';
Terminal.applyAddon(fit);
Terminal.applyAddon(fullscreen);


function new_terminal(login_panel, term_container, host, user, password, port=22) {
    let protocol    = (window.location.protocol.indexOf('https') === 0) ? 'wss' : 'ws';
    let ws_url      = protocol+'://'+window.location.host+ '/websocket';
    let terminal        = new Terminal();
    let ws          = new WebSocket(ws_url);

    ws.onopen = function (e) {
        ws.send(JSON.stringify({
            'type': 'conn',
            'data': {
                "host": host,
                "user" : user,
                "password" : password, 
                "port" : port
            }
        }));
        ws.onmessage = function (ee) {
            let json_msg = JSON.parse(ee.data);
            switch(json_msg['type']) {
                case 'conn':
                    if (json_msg['data']['status']) {
                        login_panel.hide(1, function () {
                            term_container.fadeTo(100, 0, function () {
                                terminal.open(term_container[0]);
                                terminal.fit();
                                terminal.toggleFullScreen(true);
                                term_container.fadeTo(100,1);
                            });
                            
                        });
                    }
                    break;
                case 'stdout':
                    terminal.write(json_msg['data']);
                    break;
                case 'disconnect':
                    ws.close();
                    break;
            }
        };
        
        terminal.on('data', function (data) {
            ws.send(JSON.stringify({
                'type' : 'stdin',
                'data' : data
            }));
        });
        terminal.on('resize', function () {
            ws.send(JSON.stringify({
                'type' : 'resize',
                'data' : [
                    terminal.cols,
                    terminal.rows
                ]
            }));
        });
    };
    ws.onclose = function (e){
        console.log('socket closed');
        term_container.hide(1, 'swing', function () {
            terminal.clear();
            login_panel.fadeIn(100);
        }());
    };
}
$(document).ready(function() {
    let submitBtn = $("button.btn-primary");
    let loginPanel = $("div#login-panel");
    let terminalContainer = $("div#terminal-container");
    
    submitBtn.click(function () {
        let host        = $("input#fqdnInput").val();
        let user        = $("input#userInput").val();
        let password    = $("input#passwordInput").val();
        let port        = $("input#sshPortInput").val();
        new_terminal(loginPanel, terminalContainer, host, user, password, port)
    });
    
});