var modalNew = $("div.modal#newItemModal");

//主机类型 下拉列表选择 动作
var modalNewFormRow             = modalNew.find("div.form-row");
var modalNewFormGroup           = modalNewFormRow.find("div.form-group");
var noHostFormGroup             = modalNewFormRow.find("div.form-group.noHost");
var noHostWithTemplateFormGroup = modalNewFormRow.find("div.form-group.no-host-with-template");
var noTemplateFormGroup         = modalNewFormRow.find("div.form-group.no-template");

var typeSelect                  = modalNewFormGroup.find("select#type");
var templateSelect              = modalNewFormGroup.find("select#template");

function enableAllFormGroup() {
    modalNewFormGroup.each(function () {
        $(this).children().prop('disabled', false);
    });
}

typeSelect.change(function () {
    enableAllFormGroup();
    var selected = typeSelect.find("option:selected").val();
    switch(selected) {
        case "proxy":
        case "host":
            noHostFormGroup.each(function () {
                $(this).children().prop('disabled', true);
            });
            break;
        case "template":
            noTemplateFormGroup.each(function () {
                $(this).children().prop('disabled', true);
            });
            break;
    }
});
templateSelect.change(function () {
    enableAllFormGroup();
    var selected = parseInt(typeSelect.find("option:selected").attr("data-foreign-id"));
    switch(selected) {
        case 0:
            noHostWithTemplateFormGroup.each(function () {
                $(this).children().prop('disabled', false);
            });
            break;
        default:
            noHostWithTemplateFormGroup.each(function () {
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