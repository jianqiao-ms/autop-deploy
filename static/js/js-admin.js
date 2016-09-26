/**
 * Created by jianqiao on 9/26/16.
 */

$(document).ready(function () {
    var offcanvas               = $("div.ams-container-offcanvas");
    var offcancas_toggle        = $("div.ams-rectangle-right");
    var offcancas_toggle_line   = $("div.ams-rectangle-right-in");


    offcancas_toggle.click(function () {
        var offcancasStatus = offcanvas.css('left');
        if (offcancasStatus == '-270px'){
            offcanvas.animate({left:'0px'});
            offcancas_toggle.animate({opacity:'1'});
            offcancas_toggle_line.css({left:'2px'});
        }
        if (offcancasStatus == '0px'){
            offcanvas.animate({left:'-270px'});
            offcancas_toggle.animate({opacity:'0.3'});
            offcancas_toggle_line.css({left:'6px'});
        }
    });
});