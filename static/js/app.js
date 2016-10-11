(function($) {
    'use strict';

    $(function() {
        var $fullText = $('.admin-fullText');
        $('#admin-fullscreen').on('click', function() {
            $.AMUI.fullscreen.toggle();
        });

        $(document).on($.AMUI.fullscreen.raw.fullscreenchange, function() {
            $fullText.text($.AMUI.fullscreen.isFullscreen ? '退出全屏' : '开启全屏');
        });
    });
})(jQuery);

$(document).ready(function (){
    // websocket 消息框
    var msgBox = $(".ams-header-msg-container");
    var ws = new WebSocket("ws://localhost:8888/websocket");

    ws.onmessage = function (evt) {
        msgBox.text(evt.data);
    };

    // 管理页新建按钮
    var btnNew  = $('.am-form .am-table button.am-btn-primary');
    var trNew   = $('.am-form .am-table tr#new');
    btnNew.click(function () {
        trNew.show();
    });
});

//消息提示框变量
var confirmModal            = $("#confirm");
var confirmMoadlHead        = confirmModal.find(".am-modal-hd");
var confirmMoadlBody        = confirmModal.find(".am-modal-bd");

//alert框
var alertModal              = $('#alert');
var alertModalHead          = alertModal.find('.am-modal-hd');
var alertModalBody          = alertModal.find('.am-modal-bd');

function confirm(msg, title, callback) {
    if(!arguments[2]) title = "Autop";
    confirmMoadlHead.text(title);
    confirmMoadlBody.text(msg);


    confirmModal.modal({
        relatedTarget: this,
        onConfirm:function () {
            if (typeof(callback) == "function") {
                callback();
            }
        }
    });
}


function alert(msg, title) {
    if(!arguments[2]) title = "Autop";
    alertModalHead.text(title);
    alertModalBody.text(msg);
    alertModal.modal();
}