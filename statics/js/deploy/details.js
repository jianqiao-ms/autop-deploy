$(document).ready(function(){
    $("input[value='发布']").click(function(){

        $.ajax('/deployaction')
    });
});
