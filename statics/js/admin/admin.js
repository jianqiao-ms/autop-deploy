$('#gitlabAppModel').on('show.bs.modal', function (e) {
    $(this).find('.modal-body').load('/');
});