var modalNew = $("div.modal#newItemModal");
var newItemForm = $("div#newItemModal>div>div>div.modal-body>form");
var formAction = newItemForm.attr("action");
var submitButton = $("div#newItemModal>div.modal-lg>div.modal-content>div.modal-footer>button.btn-primary");

modalNew.on("hidden.bs.modal",function () {
    $(this).find("input").each(function () {
        $(this).resetDefault()
    });
    $(this).find("select").each(function () {
        $(this).resetDefault()
    });
});

submitButton.click(function () {
    var reqJson = newItemForm.serializeJson();
    $.ajax({
        url:formAction,
        ContentType: "application/json",
        type:"POST",
        data:reqJson,
        success: function (rst) {
            if(rst.status) {
                location.reload();
            }
            else{
                console.log(rst.msg)//TODO
            }
        }
    })
});