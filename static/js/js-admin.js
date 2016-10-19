/**
 * Created by jianqiao on 9/26/16.
 */

$(document).ready(function () {
    var btnNew                  = $('button#new');                  // 新建按钮
    var trNew                   = $('tr#new');                      // 新建行
    var btnCancel               = $('button#cancel');               // cancel 按钮

    var formNewHost             = $('form#new-host');               //new-host form
    var formNewHg               = $('form#new-hg');                 //new-hg form
    var formNewProj             = $('form#new-proj');             //new-hg form

    var modalUser               = $('#userInfoModal');              //用户名密码输入框
    var btnModalUserConfirm     = $('.modal-footer .btn-primary');  //用户名密码输 modal 提交按钮

    var hostormOptions          = {
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
    var hgFormOptions           = {
        beforeSubmit:function (arr, $form, options) {
            if (formNewHg.find('[name=env]').val()=='') {
                alert('请选择主机组环境');
                return false;
            }
            if (formNewHg.find('[name=name]').val()=='') {
                alert('主机组名不能为空');
                return false;
            }
        },
        success:newHostgroup
    };
    var projFormOptions         = {
        beforeSubmit:function (arr, $form, options) {
            if (formNewProj.find('[name=repo]').val()=='') {
                alert('请输入repo地址');
                return false;
            }
        },
        success:newProject
    };

    // 按钮行为
    btnNew.click(function () {
        formNewHost.resetForm();
        trNew.show();
    });
    btnCancel.click(function () {
        trNew.hide();
    });

    // 绑定ajaxForm方法到form
    formNewHost.ajaxForm(hostormOptions);
    formNewHg.ajaxForm(hgFormOptions);
    formNewProj.ajaxForm(projFormOptions);


    btnModalUserConfirm.click(function () {
        $('#real-username').val($('#input-username').val());
        $('#real-password').val($('#input-password').val());

        modalUser.modal('hide');
        formNewHost.ajaxSubmit(hostormOptions);
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

function newHostgroup(data) {
    switch(data['code'])
    {
        case 0:
            window.location.reload();
            break;
        case 400:
            alert(data['info'], data['type']);
            break;
    }
}
function newProject(data) {
    switch(data['code'])
    {
        case 0:
            window.location.reload();
            break;
        case 400:
            alert("<code>"+data['info']+"</code>", data['type']);
            break;
    }
}