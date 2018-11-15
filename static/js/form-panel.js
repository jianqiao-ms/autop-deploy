// 标题里面的按钮
titleNewBtn = $("div.form-row button.btn-form.btn-outline-light.form-global-new:contains(新建)");
titleDelBtn = $("div.form-row button.btn-form.btn-outline-light.form-global-del:contains(删除)");

// 各行单独的按钮
var devareButton = $("div.form-row button.btn-form.btn-outline-danger:contains(删除)");

devareButton.click(function () {
    var myForm = $(this).parent().parent().parent();
    var formAction = myForm.attr("action");
    var myRow = myForm.find("div.form-row");
    var rowId = myRow.find("input.form-check-input").attr("id");

    $.ajax({
        url:formAction,
        ContentType: "application/json",
        type:"DELETE",
        data:"["+ rowId +"]",
        success: function (rst) {
            if(rst.status) {
                console.log(rst.msg);
                location.reload();
            }
            else{
                console.log("ERROR")
            }
        }
    })
});