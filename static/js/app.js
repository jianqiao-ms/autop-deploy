// websockets 方法
$(document).ready(function (){
    // websocket 消息框
    var msgBox = $(".ams-header-msg-container");
    ws = new WebSocket("ws://localhost:8888/websocket");

    ws.onmessage = function (evt) {
        msgBox.text(evt.data);
    };
});

$(document).ready(function () {
    //消息提示框变量
    var confirmModal = $("#confirm");
    var confirmMoadlHead = confirmModal.find(".am-modal-hd");
    var confirmMoadlBody = confirmModal.find(".am-modal-bd");

    //alert框
    var alertModal = $('#alertModal');
    var alertModalHead = alertModal.find('#alertModalLabel');
    var alertModalBody = alertModal.find('.modal-body');

    function confirm(msg, title, callback) {
        if (!arguments[2]) title = "Autop";
        confirmMoadlHead.text(title);
        confirmMoadlBody.text(msg);


        confirmModal.modal({
            relatedTarget: this,
            onConfirm: function () {
                if (typeof(callback) == "function") {
                    callback();
                }
            }
        });
    }


    function alert(msg, title) {
        if (arguments[1]) {
            alertModalHead.text(title);
        }
        alertModalBody.text(msg);
        alertModal.modal('show');
    }

    window.alert=alert;
});