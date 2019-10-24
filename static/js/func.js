$.fn.extend({
    // Serialize form into json data
    serializeJson: function() {
        var allInput = $(this).children("div.form-row:not(.param)").find("input:visible:enabled, select:visible:enabled");
        var formDataObject = {};
        allInput.each(function () {
            switch(true) {
                case $(this).is("select.foreign-key"):
                    whatWeWant = parseInt($(this).find(":selected").attr("data-foreign-id"));
                    break;
                case $(this).is("input[type=checkbox]"):
                    whatWeWant = $(this).prop("checked");
                    break;
                default:
                    whatWeWant = $(this).val();
            }
            if (whatWeWant === 0 || whatWeWant === "") {
                return
            }
            formDataObject[$(this).attr("name")] = whatWeWant;
        });

        var paramInput = $(this).children("div.param").find("input:visible:enabled, select:visible:enabled");
        if (paramInput.length) {
            var paramFormDataObject = {};
            paramInput.each(function () {
                switch(true) {
                    case $(this).is("select.foreign-key"):
                        whatWeWant = parseInt($(this).find(":selected").attr("data-foreign-id"));
                        break;
                    case $(this).is("input[type=checkbox]"):
                        whatWeWant = $(this).prop("checked");
                        break;
                    default:
                        whatWeWant = $(this).val();
                }
                if (whatWeWant === 0 || whatWeWant === "") {
                    return
                }
                paramFormDataObject[$(this).attr("name")] = whatWeWant;
            });
            formDataObject["param"] = paramFormDataObject;
        }

        return JSON.stringify(formDataObject)
    },

    // Reset input or select item
    resetDefault:function () {
        var elementType = $(this)[0].tagName;
        var defaultValue = $(this).attr("data-default");

        switch(elementType) {
            case "INPUT":
                $(this).val(defaultValue);
                break;
            case "SELECT":
                $(this).val(defaultValue).prop("selected", true).change();
                break;
        }
    },

    active:function () {
        if (!$(this).hasClass("active")) {
            $(this).addClass("active")
        }
    },
    deactive:function () {
        if ($(this).hasClass("active")) {
            $(this).removeClass("active")
        }
    },
    enable:function () {
        if ($(this).prop("disabled")) {
            $(this).prop("disabled", false)
        }
    },
    disable:function () {
        if (!$(this).prop("disabled")) {
            $(this).prop("disabled", true)
        }
    }
});