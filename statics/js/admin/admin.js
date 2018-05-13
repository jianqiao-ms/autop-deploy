$('#gitlabAppModel').on('show.bs.modal', function (e) {
    $(this).find('.modal-body').load('/admin/api/gitlabapps');
});

$('#gitlabAppModel').on('hidden.bs.modal', function (e) {
    $(this).find('.modal-body').html('<img class="loading" src="/statics/images/loading.gif" />');
});

$('.modal-body').on('click','button.btn-outline-primary' ,function (e) {
    var this_btn = e.currentTarget;
    var row = this_btn.parentNode.parentNode;

    var app_data = JSON.stringify({
        'gitlab_id':$(row).attr('id'),
        'deploy_name':$(row).children('.deploy_name').val(),
        'type_id':0
    });

    console.log(app_data);

    $.post('/admin/app', app_data, function (data, textStatus) {
        console.log(data);
        console.log(textStatus)
    })
});