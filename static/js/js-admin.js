/**
 * Created by jianqiao on 9/26/16.
 */

$(document).ready(function () {
    var btnNew                  = $('button#new');                  // 新建按钮
    var trNew                   = $('tr#new');                      // 新建行
    var btnSave                 = $('button#save');                 // save按钮
    var btnCancel               = $('button#cancel');               // cancel 按钮

    var formNewHost             = $('form#new-host');               //new-host form

    var modalUser               = $('#userInfoModal');              //用户名密码输入框
    var btnModalUserConfirm     = $('.modal-footer .btn-primary');  //modal 提交按钮

    var userFormOptions         = {
        beforeSubmit:function (arr, $form, options) {
            if (formNewHost.find('[name=env]').val()=='') {
                alert('请选择主机环境 或 属组');
                return false;
            }
            if (formNewHost.find('[name=ipaddr]').val()=='') {
                alert('IP地址不能为空');
                return false;
            }
        },
        success:newHost
    };

    formNewHost.ajaxForm(userFormOptions);       // 绑定ajaxForm方法到form

    btnNew.click(function () {
        formNewHost.resetForm();
        trNew.show();
    });
    btnCancel.click(function () {
        trNew.hide();
    });
    btnModalUserConfirm.click(function () {
        $('#real-username').val($('#input-username').val());
        $('#real-password').val($('#input-password').val());

        modalUser.modal('hide');
        formNewHost.ajaxSubmit(userFormOptions);
    });

});

function newHost(data) {
    switch(data['code'])
    {
        case 0:
            window.location.reload();
            break;
        case 100:
            alert('无法连接到主机,请检查主机alive状态');
            break;
        case 200:
        case 101:
            alert('ip 地址格式错误');
            break;
        case 300:
        case 301:
            $('#userInfoModal').modal('show');
            break;
        case 310:
            alert('端口不正确');
            break;
        case 400:
            alert(data['info'], data['type']);
            break;
    }
}