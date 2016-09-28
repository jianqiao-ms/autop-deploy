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
    var msgBox = $(".ams-header-msg-container");
    var ws = new WebSocket("ws://localhost:8888/websocket");

    ws.onmessage = function (evt) {
        msgBox.text(evt.data);
    };
});