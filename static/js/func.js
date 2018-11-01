$.fn.extend({
    // Serialize form into json data
    serializeJson: function() {
        let allInput = $(this).find("input:visible, select:visible");
        let formDataObject = Object();
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
            let _ = {};
            _[$(this).attr("name")] = whatWeWant;

            $.extend(formDataObject, _);
        });
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
