let projectSelect               = newInventoryFormRow.find("select#project");
let nameInput                   = newInventoryFormRow.find("input#visiblename");
let standaloneCheckbox          = newInventoryFormRow.find("input#standalone");

function FolderTreeChild(name, type="tree") {
    if (type !== "tree") {
        return $('<div class="col-sm-12"><i class="far fa-file"></i> <a>' + name + '</a></div>')
    }
    return $('<div class="col-sm-12"><i class="far fa-folder-open"></i> <a>' + name + '</a>' +
                '<select class="form-control-sm tag-select float-right" name="'+ name +'" disabled>' +
                    '<option>Public</option>' +
                    '<option>Product</option>' +
                    '<option>Parent</option>' +
                '</select>' +
            '</div>')
}
function FolderTree(rootname="Root") {
    this.tree = $("div.tree");
    this.root = $("div.tree>.col-sm-12>a");
    this.childZone = $("div.tree>.col-sm-12>.form-row");
    this.addChild = function (name, type) {
        this.childZone.append(FolderTreeChild(name, type));
    };
    this.resetDefault = function () {
        this.root.html("Root");
        this.childZone.html("");
    };
    this.update = function (selectedOption) {
        let selectedGitlabProjectId = selectedOption.attr("data-foreign-id");
        let selectedGitlabProjectName = selectedOption.val().substring(selectedOption.val().lastIndexOf(' / ') + 3);
        let tree = this;

        this.resetDefault();
        this.root.html(selectedGitlabProjectName);
        $.ajax({
            type: "GET",
            url: "/api/v1/gitlab/projects/" + selectedGitlabProjectId + "/repository/tree",
            beforeSend: function (request) {
                request.setRequestHeader("Content-Type", "application/json");
            },
            success: function (rst) {
                let fileArray = JSON.parse(rst);

                if (fileArray.length === 0) {
                    console.log("空项目");
                    standaloneCheckbox.parent().click();
                    return
                }

                $(fileArray).each(function () {
                    tree.addChild($(this)[0].name, $(this)[0].type)
                });
                tree.tree.show();
            }
        });
    }
}

let folderTree                  = new FolderTree();

projectSelect.change(function () {
    let selectedOption  = projectSelect.find("option:selected");
    // let project_name    = selectedOption.val().substring(selectedOption.val().lastIndexOf(' / ')+3);
    let project_name    = selectedOption.val();
    if (selectedOption.val() === "Choose...") {
        nameInput.val("");
        folderTree.resetDefault();
        if(!standaloneCheckbox.is(":checked")) {
            standaloneCheckbox.parent().click();
        }
    } else {
        if(!standaloneCheckbox.is(":checked")) {
            standaloneCheckbox.parent().click();
        }
        nameInput.val(project_name);
        folderTree.update(selectedOption);
    }
});


standaloneCheckbox.change(function () {
    let selectedOption  = projectSelect.find("option:selected");

    if (!standaloneCheckbox.prop("checked")) {
        if (selectedOption.val() === "Choose...") {
            console.log("Alerm! Choose project first!");
            standaloneCheckbox.prop("checked", true);
        } else {
            standaloneCheckbox.parent().deactive();
        }
    }

    let tagSelect = newInventoryFormRow.find("select.tag-select");
    if (standaloneCheckbox.prop("checked")) {
        tagSelect.each(function () {
            $(this).prop("disabled", true)
        });
    } else {
        tagSelect.each(function () {
            $(this).prop("disabled", false)
        });
    }
});

/* 从API模块获取数据填充modal组件
* =====================================================================================================================
* =====================================================================================================================
*/

// 从API模块获取数据填充modal组件
function gitlabProjectOption(gitlabProject) {
    return '<option data-foreign-id="'+ gitlabProject.id +'">'+ gitlabProject.name_with_namespace +'</option>'
}

$(document).ready(function () {
    titleNewBtn.disable();
    $.ajax({
        type: "GET",
        url: "/api/v1/gitlab/projects?simple=true",
        success: function (rst) {
            let allProjects = JSON.parse(rst);
            let c = allProjects.length;
            while (c--) {
                projectSelect.append(gitlabProjectOption(allProjects[c]))
            }
            titleNewBtn.enable();
        }
    });
});