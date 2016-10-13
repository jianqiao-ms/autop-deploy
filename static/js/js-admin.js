/**
 * Created by jianqiao on 9/26/16.
 */

$(document).ready(function () {
    var offcanvas               = $("div.ams-container-offcanvas");
    var offcancasToggle         = $("div.ams-rectangle-right");
    var offcancasToggleLine     = $("div.ams-rectangle-right-in");
    var contentTable            = $("div.ams-container-global table.am-table-bordered");
    var contentTableTd          = contentTable.find('td');

    $(window).resize(function () {
        if ($(window).width() > 640) {
            offcanvas.css({left:0})
        }
        else {
            offcanvas.css({left:'-230px'})
        }
    });

    offcancasToggle.click(function () {
        var offcancasStatus = offcanvas.css('left');
        if (offcancasStatus == '-230px'){
            offcanvas.animate({left:'0px'});
            offcancasToggle.animate({opacity:'1'});
            offcancasToggleLine.animate({left:'2px'});
        }
        if (offcancasStatus == '0px'){
            offcanvas.animate({left:'-230px'});
            offcancasToggle.animate({opacity:'0.3'});
            offcancasToggleLine.animate({left:'6px'});
        }
    });

    // 新建按钮
    var btnNew  = $('.am-form .am-table button.am-btn-primary');
    var trNew   = $('.am-form .am-table tr#new');
    btnNew.click(function () {
        trNew.show();
    });


    function newHost(data) {
        switch(data['code'])
        {
            case 100:
                alert('无法连接到主机,请检查主机alive状态');
                break;
            case 200:
            case 101:
                alert('ip 地址格式错误');
                break;
            case 300:
                userinfoModal.modal({
                    onConfirm:function () {
                        $('#real-username').val($('#input-username').val());
                        $('#real-password').val($('#input-password').val());
                        formNew.ajaxSubmit(newHost);
                    }
                });
                break;
            case 301:
                alert('端口不正确');
                break;
            case 400:
                alert(data['info'], data['type']);
                break;
        }
    }
    //用户名密码输入框
    var userinfoModal = $('#userinfoModal');
    //新建form
    var formNew = $('.am-form');
    formNew.ajaxForm(newHost);
});