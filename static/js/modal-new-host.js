var modalNew = $("div.modal#newItemModal");

//主机类型 下拉列表选择 动作
var modalNewFormRow = modalNew.find("div.form-row");
var typeSelect = modalNewFormRow.find("div.form-group>select#type");
var hostNeededForm = modalNewFormRow.find("div.form-group.host-needed");
var templateNeededForm = modalNewFormRow.find("div.form-group.template-needed");
typeSelect.change(function () {
    modalNewFormRow.each(function () {
        $(this).find("div.form-group").children().prop('disabled', false);
    });

    var selected = typeSelect.find("option:selected").val();
    switch(selected) {
        case "proxy":
        case "host":
            templateNeededForm.each(function () {
                $(this).children().prop('disabled', true);
            });
            break;
        case "template":
            hostNeededForm.each(function () {
                $(this).children().prop('disabled', true);
            });
            break;
    }
});

//SSH验证类型 下拉列表选择 动作
var sshAuthTypeSelect = modalNewFormRow.find("div.form-group>select#ssh_auth_type");
var passwordInput = modalNewFormRow.find("div.form-group.ssh-password-show");
var keyInput = modalNewFormRow.find("div.form-group.ssh-key-show");

sshAuthTypeSelect.change(function () {
    console.log("change");
    var selected = sshAuthTypeSelect.find("option:selected").val();
    console.log(selected);
    switch(selected) {
        case "password":
            keyInput.addClass("d-none");
            passwordInput.removeClass("d-none");
            break;
        case "rsa_key":
            passwordInput.addClass("d-none");
            keyInput.removeClass("d-none");
            break;
    }
});