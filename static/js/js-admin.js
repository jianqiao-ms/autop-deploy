/**
 * Created by jianqiao on 9/26/16.
 */

$(document).ready(function () {
    var offcanvas               = $("div.ams-container-offcanvas");
    var offcancasToggle        = $("div.ams-rectangle-right");
    var offcancasToggleLine   = $("div.ams-rectangle-right-in");

    $(window).resize(function () {
        if ($(window).width() > 640) {
            offcanvas.css({left:0})
        }
        else {
            offcanvas.css({left:'-270px'})
        }
    });

    offcancasToggle.click(function () {
        var offcancasStatus = offcanvas.css('left');
        if (offcancasStatus == '-270px'){
            offcanvas.animate({left:'0px'});
            offcancasToggle.animate({opacity:'1'});
            offcancasToggleLine.animate({left:'2px'});
        }
        if (offcancasStatus == '0px'){
            offcanvas.animate({left:'-270px'});
            offcancasToggle.animate({opacity:'0.3'});
            offcancasToggleLine.animate({left:'6px'});
        }
    });


});