newInventoryModal       = $("div.modal#newInventoryModal");
newInventoryForm        = $("div#newInventoryModal>div>div>div.modal-body>form");
newInventoryFormRow     = newInventoryForm.find("div.form-row");
newInventoryFormGroup   = newInventoryFormRow.find("div.form-group");
visibleNameInput        = newInventoryFormRow.find("input#visiblename");
formAction              = newInventoryForm.attr("action");



let submitButton        = $("div#newInventoryModal>div.modal-lg>div.modal-content>div.modal-footer>button.btn-primary");

newInventoryModal.on("hidden.bs.modal",function () {
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