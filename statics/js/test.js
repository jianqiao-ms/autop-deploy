var ws = new WebSocket("ws://localhost:60000/test");
      ws.onopen = function() {
         ws.send("Hello, world");
      };
      ws.onmessage = function (evt) {
         console.log(evt.data);
};