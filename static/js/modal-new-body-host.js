let modalNewFormRow             = modalNew.find("div.form-row");
let modalNewFormGroup           = modalNewFormRow.find("div.form-group");

let noHostFormGroup             = modalNewFormRow.find(".noHost");
let noWithTemplateFormGroup     = modalNewFormRow.find(".no-with-template");
let noTemplateFormGroup         = modalNewFormRow.find(".no-type-template");


let districtSelect              = modalNewFormRow.find("select#district");
let typeSelect                  = modalNewFormRow.find("select#type");
let templateSelect              = modalNewFormRow.find("select#template");
let sshUserInput                = modalNewFormRow.find("input#ssh_user");
let sshPortInput                = modalNewFormRow.find("input#ssh_port");
let sshAuthTypeSelect           = modalNewFormRow.find("select#ssh_auth_type");
let sshPasswordInput            = modalNewFormRow.find("input#ssh_password");
let sshKeyInput                 = modalNewFormRow.find("input#ssh_key");
let sshPasswordFormRow          = modalNewFormRow.find("div.form-group.ssh-password-show");
let sshKeyFormRow               = modalNewFormRow.find("div.form-group.ssh-key-show");

function enableAllFormGroup() {
    modalNewFormGroup.each(function () {
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
            sshKeyFormRow.addClass("d-none");
            sshPasswordFormRow.removeClass("d-none");
            break;
        case "rsa_key":
            sshPasswordFormRow.addClass("d-none");
            sshKeyFormRow.removeClass("d-none");
            break;
    }
});