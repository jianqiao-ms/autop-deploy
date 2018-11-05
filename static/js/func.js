$.fn.extend({
    // Serialize form into json data
    serializeJson: function() {
        let allInput = $(this).find("div[class='form-row border-bottom'],div[class='border-bottom form-row']").find("input:visible:enabled, select:visible:enabled");
        let formDataObject = {};
        allInput.each(function () {
            let whatWeWant = $(this).is("select.foreign-key")?parseInt($(this).find(":selected").attr("data-foreign-id")):$(this).val();
            if ($(this).is("input[type=checkbox]")) {
                whatWeWant = $(this).prop("checked");
            }
            if (whatWeWant === 0) {
                return
            }
            if (whatWeWant === "") {
                return
            }
            formDataObject[$(this).attr("name")] = whatWeWant;
        });

        let paramInput = $(this).find("div.param").find("input:visible:enabled, select:visible:enabled");
        let paramFormDataObject = {};
        paramInput.each(function () {
            let whatWeWant = $(this).is("select.foreign-key")?parseInt($(this).find(":selected").attr("data-foreign-id")):$(this).val();
            if ($(this).is("input[type=checkbox]")) {
                whatWeWant = $(this).prop("checked");
            }
            if (whatWeWant === 0) {
                return
            }
            if (whatWeWant === "") {
                return
            }
            paramFormDataObject[$(this).attr("name")] = whatWeWant;
        });

        formDataObject["param"] = paramFormDataObject;
        return JSON.stringify(formDataObject)
    },

    // Reset input or select item
    resetDefault:function () {
        let elementType = $(this)[0].tagName;
        let defaultValue = $(this).attr("data-default");

        switch(elementType) {
            case "INPUT":
                $(this).val(defaultValue);
                break;
            case "SELECT":
                $(this).val(defaultValue).prop("selected", true).change();
                break;
        }
    }
});
