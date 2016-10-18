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

    formNewHost.ajaxForm(newHost);                                  // 绑定ajaxForm方法到form

    btnNew.click(function () {
        trNew.show();
    });
    btnCancel.click(function () {
        trNew.hide();
    });
    btnModalUserConfirm.click(function () {
        $('#real-username').val($('#input-username').val());
        $('#real-password').val($('#input-password').val());

        console.log($('#real-username').val());
        console.log($('#real-password').val());
        console.log($('#input-username').val());
        if ($('#input-password').val()=='  ') {
            console.log('空格');
        }

        formNewHost.ajaxSubmit(newHost);
        modalUser.modal('hide');
    });


});

function newHost(data) {
    console.log(data['code']);
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
        case 301:
            console.log('来了');
            modal($('#userInfoModal'),'认证失败');
            console.log('走了');
            break;
        case 310:
            alert('端口不正确');
            break;
        case 400:
            alert(data['info'], data['type']);
            break;
    }
}

function modal($modal, title, reset) {
    if(!arguments[1]) title = "Autop";
    if(!arguments[2]) reset = true;

    if(reset) {
        $modal.find('form').resetForm();
    }
    if($modal.find('.modal-title').text()!=title) {
        $modal.find('.modal-title').text(title);
    }
    $modal.modal('show');
}