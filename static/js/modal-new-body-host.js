
let noHostFormGroup             = newInventoryFormRow.find(".noHost");
let noWithTemplateFormGroup     = newInventoryFormRow.find(".no-with-template");
let noTemplateFormGroup         = newInventoryFormRow.find(".no-type-template");


let districtSelect              = newInventoryFormRow.find("select#district");
let typeSelect                  = newInventoryFormRow.find("select#type");
let templateSelect              = newInventoryFormRow.find("select#template");
let sshUserInput                = newInventoryFormRow.find("input#ssh_user");
let sshPortInput                = newInventoryFormRow.find("input#ssh_port");
let sshAuthTypeSelect           = newInventoryFormRow.find("select#ssh_auth_type");
let sshPasswordInput            = newInventoryFormRow.find("input#ssh_password");
let sshKeyInput                 = newInventoryFormRow.find("input#ssh_key");
let sshPasswordFormGroup        = newInventoryFormRow.find("div.form-group.ssh-password-show");
let sshKeyFormGroup             = newInventoryFormRow.find("div.form-group.ssh-key-show");

function enableAllFormGroup() {
    newInventoryFormGroup.each(function () {
        $(this).children().prop('disabled', false);
    });
}

//选择类型 下拉列表选择 动作
typeSelect.change(function () {
    enableAllFormGroup();
    let selected = typeSelect.find("option:selected").val();
    switch(selected) {
        case "proxy":
        case "host":
            noHostFormGroup.each(function () {
                $(this).prop('disabled', true);
            });
            break;
        case "template":
            noTemplateFormGroup.each(function () {
                $(this).resetDefault();
                $(this).prop('disabled', true);
            });
            break;
    }
});

//选择模板 下拉列表选择 动作
templateSelect.change(function () {
    let selected = parseInt(templateSelect.find("option:selected").attr("data-foreign-id"));

    $.ajax({
        url:"/inventory/host?id=" + selected,
        contentType: "application/json",
        type:"GET",
        success: function (rst) {
            let templatesObject = JSON.parse(rst)[0];

            if (selected>0) {
                districtSelect.val(templatesObject.district.visiblename).prop("selected", true).change();
                sshUserInput.val(templatesObject.ssh_user);
                sshPortInput.val(templatesObject.ssh_port);
                sshAuthTypeSelect.val(templatesObject.ssh_auth_type).prop("selected", true).change();
                sshPasswordInput.val(templatesObject.ssh_password);
                sshKeyInput.val(templatesObject.ssh_key);

                noWithTemplateFormGroup.each(function () {
                    $(this).prop('disabled', true);
                });
            } else {
                noWithTemplateFormGroup.each(function () {
                    $(this).resetDefault();
                    $(this).prop('disabled', false);
                });
            }
        }
    });



});

//SSH验证类型 下拉列表选择 动作
sshAuthTypeSelect.change(function () {
    let selected = sshAuthTypeSelect.find("option:selected").val();
    switch(selected) {
        case "password":
            sshKeyFormGroup.addClass("d-none");
            sshPasswordFormGroup.removeClass("d-none");
            break;
        case "rsa_key":
            sshPasswordFormGroup.addClass("d-none");
            sshKeyFormGroup.removeClass("d-none");
            break;
    }
});