function new_terminal() {
    let protocol    = (window.location.protocol.indexOf('https') === 0) ? 'wss' : 'ws';
    let ws_url      = protocol+'://'+window.location.host+ '/recordwebsocket';
    let ws          = new WebSocket(ws_url);
    let terminal    = new Terminal();
    // let records     = {};
    
    ws.onopen = function (e) {
        terminal.fit();
        ws.onmessage = function (ee) {
            let records_line = ee.data;
            let records = records_line.split('endtimestamp\n');
            // console.log(records);
            let startTimestamp = parseInt(records[0].substring(11, 22));

            // for (let i=0; i < records.length; i++) {
            //     let newTimestamp = parseInt(records[i].substring(11, 22));
            //     let timeDelt = newTimestamp - startTimestamp;
            //     console.log(timeDelt)
                // window.setTimeout(console.log(timeDelt), timeDelt);
                // setTimeout(terminal.write(records[i].substring(22)), timeDelt);
                // setTimeout(function () {
                //     terminal.write('log')
                // } , timeDelt);
            // }

            // for (var i = 0; i < 5; i++) {
            //     setTimeout(function (){
            //         console.log(i);
            //         },1000);
            // }

            for (let i=0; i < records.length; i++) {
                let newTimestamp = parseInt(records[i].substring(11, 22));
                let timeDelt = newTimestamp - startTimestamp;
                (function (__timeDelt) {
                    setTimeout(function (){
                        terminal.write(records[i].substring(22))
                    }, __timeDelt);
                })(timeDelt)
            }

        };
    };

    window.onresize = function() { 
        terminal.fit();
    };
    terminal.open(document.getElementById('terminal-container'));
}

$(document).ready(function() {
    Terminal.applyAddon(fit);
    new_terminal();

    // for (var i = 0; i < 5; i++) {
    //     (function(ii){   //立刻执行函数
    //         setTimeout(function (){
    //             console.log(ii);
    //         },ii * 1000);
    //     })(i);
    // }
});