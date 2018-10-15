var modalNewFormRow             = modalNew.find("div.form-row");
var modalNewFormGroup           = modalNewFormRow.find("div.form-group");

var noHostFormGroup             = modalNewFormRow.find(".noHost");
var noWithTemplateFormGroup     = modalNewFormRow.find(".no-with-template");
var noTemplateFormGroup         = modalNewFormRow.find(".no-type-template");


var districtSelect              = modalNewFormRow.find("select#district");
var typeSelect                  = modalNewFormRow.find("select#type");
var templateSelect              = modalNewFormRow.find("select#template");
var sshUserInput                = modalNewFormRow.find("input#ssh_user");
var sshPortInput                = modalNewFormRow.find("input#ssh_port");
var sshAuthTypeSelect           = modalNewFormRow.find("select#ssh_auth_type");
var sshPasswordInput            = modalNewFormRow.find("input#ssh_password");
var sshKeyInput                 = modalNewFormRow.find("input#ssh_key");
var sshPasswordFormRow          = modalNewFormRow.find("div.form-group.ssh-password-show");
var sshKeyFormRow               = modalNewFormRow.find("div.form-group.ssh-key-show");

function enableAllFormGroup() {
    modalNewFormGroup.each(function () {
        $(this).children().prop('disabled', false);
    });
}

//选择类型 下拉列表选择 动作
typeSelect.change(function () {
    enableAllFormGroup();
    var selected = typeSelect.find("option:selected").val();
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
    var selected = parseInt(templateSelect.find("option:selected").attr("data-foreign-id"));

    $.ajax({
        url:"/assets/host?id=" + selected,
        contentType: "application/json",
        type:"GET",
        success: function (rst) {
            var templatesObject = JSON.parse(rst)[0];

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
    var selected = sshAuthTypeSelect.find("option:selected").val();
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