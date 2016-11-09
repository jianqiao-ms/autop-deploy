/**
 * Created by jianqiao on 9/26/16.
 */


$(document).ready(function () {
    trNew                       = $('tr#new');                      // 新建行
    var btnNew                  = $('button#new');                  // 新建按钮
    var btnCancel               = $('button#cancel');               // cancel 按钮
    var formNewHost             = $('form#new-host');               //new-host form
    var formNewHg               = $('form#new-hg');                 //new-hg form
    var formNewProj             = $('form#new-proj');               //new-hg form

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
    switch(data['code']) {
        case 0:
            window.location.reload();
            break;
        case 11:
            var _t_env  = trNew.find('select[name=env]').val();
            var _t_name = trNew.find('input[name=name]').val();
            alert(_t_env+' 已经存在 '+_t_name+' 主机组', '数据冲突');
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
            alert("<pre>"+data['info']+"</pre>", data['type']);
            break;
    }
}

function newHostgroup(data) {
    switch(data['code']) {
        case 0:
            window.location.reload();
            break;
        case 11:
            var _t_env  = trNew.find('select[name=env]').val();
            var _t_name = trNew.find('input[name=name]').val();
            alert(_t_env+' 已经存在 '+_t_name+' 主机组', '数据冲突');
            break;
        case 400:
            alert("<pre>"+data['info']+"</pre>", data['type']);
            break;
    }
}
function newProject(data) {
    var _t_repo = trNew.find('input[name=repo]').val();
    var _t_name = trNew.find('input[name=alias]').val();
    switch(data['code']) {
        case 0:
            window.location.reload();
            break;
        case 1:
            alert('项目 '+_t_name+' 本地repo已存在,请手动删除再重新添加');
            break;
        case 11:

            switch(data['column']) {
                case 'alias':
                    alert('名称 '+_t_name+' 已经存在', '数据冲突');
                    break;
                case 'repo':
                    alert('项目repo '+_t_repo+' 已经存在', '数据冲突');
                    break;
            }
            break;
        case 100:
            alert('请确认项目地址是否有效', 'Invalid Repository');
            break;
        case 400:
            alert("<pre>"+data['info']+"</pre>", data['type']);
            break;
    }
}