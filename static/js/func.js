$.fn.extend({
    // Serialize form into json data
    serializeJson: function() {
        var allInput = $(this).find("input:visible, select:visible");
        var formDataObject = Object();
        allInput.each(function () {
            var whatWeWant = $(this).is("select.foreign-key")?parseInt($(this).find(":selected").attr("data-foreign-id")):$(this).val();
            if (whatWeWant === 0) {
                return
            }
            if (whatWeWant === "") {
                return
            }
            var _ = {};
            _[$(this).attr("name")] = whatWeWant;

            $.extend(formDataObject, _);
        });
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
    }
});
