var modalNewFormRow             = modalNew.find("div.form-row");

var projectSelect               = modalNewFormRow.find("select#project");
var nameInput                   = modalNewFormRow.find("input#visiblename");


//选择项目 下拉列表选择 动作
projectSelect.change(function () {
    var selected = projectSelect.find("option:selected").val();
    project_name= selected.substring(selected.lastIndexOf(' / ')+3);
    nameInput.val(project_name);
});