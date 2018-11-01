let modalNew = $("div.modal#newItemModal");
let newItemForm = $("div#newItemModal>div>div>div.modal-body>form");
let formAction = newItemForm.attr("action");
let submitButton = $("div#newItemModal>div.modal-lg>div.modal-content>div.modal-footer>button.btn-primary");

modalNew.on("hidden.bs.modal",function () {
    $(this).find("select").each(function () {
        $(this).resetDefault()
    });
    $(this).find("input").each(function () {
        $(this).resetDefault()
    });
});

submitButton.click(function () {
    let reqJson = newItemForm.serializeJson();

    console.log(reqJson);

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