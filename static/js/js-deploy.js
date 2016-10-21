/**
 * Created by jianqiao on 9/26/16.
 */

$(document).ready(function () {
    trNew                       = $('tr#new');                      // 新建行
    var btnNew                  = $('button#new');                  // 新建按钮
    var btnCancel               = $('button#cancel');               // cancel 按钮
    var formNewAutoRule         = $('#new-auto-rule');
    var navTabs                 = $('.nav-tabs');
    var tabContent              = $('.tab-content');

    navTabs.find(':first').addClass('active');
    tabContent.find(':first').addClass('active');

    // 按钮行为
    btnNew.click(function () {
        formNewAutoRule.resetForm();
        trNew.show();
    });
    btnCancel.click(function () {
        trNew.hide();
    });
});