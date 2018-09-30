var newItemForm = $("div#newItemModal>div>div>div.modal-body>form");
var formAction = newItemForm.attr("action");
var submitButton = $("div#newItemModal>div.modal-lg>div.modal-content>div.modal-footer>button.btn-primary");

submitButton.click(function () {
    var reqJson = newItemForm.serializeJson();

    //
    //
    //
    //
    //
    //
    //
    //
    //
    // var reqArray = newItemForm.serializeArray();
    // var reqObject = Object();
    // reqArray.forEach(function (formObject, index, array) {
    //     _ = {};_[formObject.name] = formObject.is("select")?formObject.selected.attr("id"):formObject.value;
    //     $.extend(reqObject, _)
    // });
    // var reqJSON = JSON.stringify(reqObject);

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