var ws = new WebSocket("ws://192.168.2.200:60000/websocket");
var block_terminal = $("div.terminal");

ws.onopen = function() {
   ws.send("ls");
};
ws.onmessage = function (evt) {
   console.log(evt.data);
   block_terminal.append(evt.data);
};
