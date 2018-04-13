$(document).ready(function() {
    $("input[value='发布']").click(function () {

        var pid = $("tr.pdetail").attr('id');
        var commit = $("select option:selected").attr('id');

        window.location.href = "/deploy?gitlab_id=" + pid + '&' + 'commit=' + commit;
    })
});