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

    
    //新建form
    var formNew = $('.am-form');
    formNew.ajaxForm(function () {
    });

});