/**
 * Created by jianqiao on 9/26/16.
 */

$(document).ready(function () {
    trNew = $('tr#new');                      // 新建行
    var btnNew = $('button#new');                  // 新建按钮
    var btnCancel = $('button#cancel');               // cancel 按钮
    var formNewAutoRule = $('#new-auto-rule');              // new auto rule form
    var navTabs = $('.nav-tabs');
    var tabContent = $('.tab-content');

    var autoRuleFormOptions = {
        beforeSubmit: function (arr, $form, options) {
            if (formNewAutoRule.find('[name=project]').val() == '') {
                alert('请选择项目');
                return false;
            }
            if (formNewAutoRule.find('[name=Container]').val() == '') {
                alert('请选择主机 或 主机组');
                return false;
            }
        },
        success: newAutoRule
    };

    // 按钮行为
    btnNew.click(function () {
        formNewAutoRule.resetForm();
        trNew.show();
    });
    btnCancel.click(function () {
        trNew.hide();
    });

    // 绑定ajaxForm方法到form
    formNewAutoRule.ajaxForm(autoRuleFormOptions);
    function newAutoRule(data) {
        switch (data['code']) {
            case 0:
                window.location.reload();
                break;
            case 11:
                var _t_proj = trNew.find('select[name=project]').text();
                switch (data['project_id']) {
                    case 'alias':
                        alert('项目 ' + _t_proj + ' 已经存在', '数据冲突');
                        break;
                }
                break;
            case 400:
                alert("<pre>" + data['info'] + "</pre>", data['type']);
                break;
        }
    }
});