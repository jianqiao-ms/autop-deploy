// websockets 方法
$(document).ready(function (){
    // websocket 消息框
    // var msgBox = $(".ams-header-msg-container");
    // ws = new WebSocket("ws://localhost:8888/websocket");
    //
    // ws.onmessage = function (evt) {
    //     msgBox.text(evt.data);
    // };
});

$(document).ready(function () {
    //消息提示框变量
    var confirmModal = $("#confirmModal");
    var confirmMoadlHead = confirmModal.find(".modal-title");
    var confirmMoadlBody = confirmModal.find(".modal-body");
    var btnConfirmModal = confirmModal.find(".btn-warning");

    //alert框
    var alertModal = $('#alertModal');
    var alertModalHead = alertModal.find('#alertModalLabel');
    var alertModalBody = alertModal.find('.modal-body');

    function confirm(msg, title) {
        if (!arguments[1]) title = "Autop";
        confirmMoadlHead.text(title);
        confirmMoadlBody.text(msg);
        confirmModal.modal('show');
    }
    btnConfirmModal.click(function () {
        confirmModal.modal('hide');
    });


    function alert(msg, title) {
        if (arguments[1]) {
            alertModalHead.text(title);
        }
        alertModalBody.html(msg);
        alertModal.modal('show');
    }

    window.alert=alert;
    window.confirm=confirm;
});