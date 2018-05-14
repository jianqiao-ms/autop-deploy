// Modal动作 新建App
$('#gitlabAppModel').on('show.bs.modal', function (e) {
    $(this).find('.modal-body').load('/admin/api/gitlabapps');
});
$('#gitlabAppModel').on('hidden.bs.modal', function (e) {
    $(this).find('.modal-body').html('<img class="loading" src="/statics/images/loading.gif" />');
});

// Modal-body 按钮动作 新建App
$('#gitlabAppModel').on('click','button.btn-outline-primary' ,function (e) {
    var this_btn = e.currentTarget;
    $(this_btn).toggleClass('disabled', true);
    $(this_btn).html('<img class="loading loading-btn" src="/statics/images/loading.gif" />');
    var row = this_btn.parentNode.parentNode;

    var app_data = JSON.stringify({
        'gitlab_id':$(row).attr('id'),
        'deploy_name':$(row).children('.deploy_name').val(),
        'type_id':0
    });
    //
    console.log(app_data);

    $.post('/admin/app', app_data, function (data) {
        if (data === 'OK') {
            $(this_btn).html('Exsit');
        } else {
            $(this_btn).toggleClass('btn-outline-primary', false);
            $(this_btn).toggleClass('btn-outline-danger', true);
            $(this_btn).html('Failed');
        }
    })
});


// Modal动作 新建AppType
// $('#gitlabAppTypeModel').on('show.bs.modal', function (e) {
//     $(this).find('.modal-body').load('/admin/api/gitlabapps');
// });

// Modal-body 按钮动作 新建AppType
$('#gitlabAppTypeModel').on('click','button.btn-outline-primary' ,function (e) {
    var apptype = $('#gitlabAppTypeModel').find('#apptype').val();
    var this_btn = e.currentTarget;
    // $(this_btn).toggleClass('disabled', true);
    // $(this_btn).html('<img class="loading loading-btn" src="/statics/images/loading.gif" />');

    var apptype_data = JSON.stringify({
        'name':apptype
    });
    //
    console.log(apptype_data);

    $.post('/admin/app_type', apptype_data, function (data) {
        if (data === 'OK') {
            $(this_btn).html('Exsit');
        } else {
            $(this_btn).toggleClass('btn-outline-primary', false);
            $(this_btn).toggleClass('btn-outline-danger', true);
            $(this_btn).html('Failed');
        }
    })
});