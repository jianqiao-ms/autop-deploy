var modalNewFormRow             = modalNew.find("div.form-row");

var projectSelect               = modalNewFormRow.find("select#project");
var nameInput                   = modalNewFormRow.find("input#visiblename");
var repoInput                   = modalNewFormRow.find("input#repo");
var standaloneCheckbox          = modalNewFormRow.find("input#standalone");

var folderTreeRow               = $("div#folder-tree");
var FolderTree                  = $("div.tree>div.col-sm-12>.form-row");
function folderTreeChild(name, type) {
    if (type !== "tree") {
        return $('<div class="col-sm-12"><i class="far fa-file"></i> <a>' + name + '</a></div>')
    }
    else {
        return $('<div class="col-sm-12"><i class="far fa-folder-open"></i> <a>' + name + '</a></div>')
    }
}
$.fn.extend({
    flush: function () {
        $(this).html("")
    }
});
$.fn.extend({
    addChild: function (name, type) {
            $(this).append(folderTreeChild(name, type))
    }
});


//选择项目 下拉列表选择 动作
projectSelect.change(function () {
    var selected = projectSelect.find("option:selected").val();
    project_name= selected.substring(selected.lastIndexOf(' / ')+3);
    nameInput.val(project_name);
    FolderTree.flush();
    folderTreeRow.hide();
    if(!standaloneCheckbox.is(":checked")) {
        var selectedGitlabProjectId = projectSelect.find("option:selected").attr("data-foreign-id");
        var projectTree = Object();
        $.ajax({
            type:"GET",
            url:"/api/gitlab/projects/" + selectedGitlabProjectId + "/repository/tree",
            beforeSend: function(request) {
                request.setRequestHeader("Content-Type", "application/json");
            },
            success: function (rst) {
                fileArray = JSON.parse(rst);
                FolderTree.flush();
                $(fileArray).each(function () {
                    FolderTree.addChild($(this)[0].name, $(this)[0].type)
                });
                folderTreeRow.show();
            }
        });
    }
});

standaloneCheckbox.change(function () {
    if(!standaloneCheckbox.is(":checked")) {
        var selectedGitlabProjectId = projectSelect.find("option:selected").attr("data-foreign-id");
        var projectTree = Object();
        $.ajax({
            type:"GET",
            url:"/api/gitlab/projects/" + selectedGitlabProjectId + "/repository/tree",
            beforeSend: function(request) {
                request.setRequestHeader("Content-Type", "application/json");
            },
            success: function (rst) {
                fileArray = JSON.parse(rst);

                if (fileArray.length === 0) {
                    console.log("空项目");
                    standaloneCheckbox.parent().click();
                    return
                }

                FolderTree.flush();
                $(fileArray).each(function () {
                    FolderTree.addChild($(this)[0].name, $(this)[0].type)
                });
                folderTreeRow.show();
            }
        });
    }
    else {
        FolderTree.flush();
        folderTreeRow.hide();
    }
});