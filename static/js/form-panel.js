// 标题里面的按钮
let titleBtnNew = $("div.form-row button.btn-form.btn-outline-light.form-global-new:contains(新建)");
let titleBtnDel = $("div.form-row button.btn-form.btn-outline-light.form-global-del:contains(删除)");

// 各行单独的按钮
let deleteButton = $("div.form-row button.btn-form.btn-outline-danger:contains(删除)");


deleteButton.click(function () {
    let myForm = $(this).parent().parent().parent();
    let formAction = myForm.attr("action");
    let myRow = myForm.find("div.form-row");
    let rowId = myRow.find("input.form-check-input").attr("id");

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



