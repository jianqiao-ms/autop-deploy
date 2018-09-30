$.fn.extend({
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
    }
});
